from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError


def init_db(base: DeclarativeMeta, engine: Engine):
    base.metadata.create_all(bind=engine)


def _extract_model_params(defaults: dict | None, **kwargs):
    defaults = defaults or {}
    params = {}

    params.update(kwargs)
    params.update(defaults)

    return params


def _create_object_from_params(session, model, lookup, params, lock=False):
    obj = model(**params)
    session.add(obj)

    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        query = session.query(model).filter_by(**lookup)

        if lock:
            query = query.with_for_update()
        try:
            obj = query.one()
        except NoResultFound:
            raise
        else:
            return obj, False
    else:
        return obj, True


def get_or_create(
    session: Session,
    model: DeclarativeBase,
    defaults: dict | None = None,
    **unique_kwargs
) -> tuple[DeclarativeMeta, bool]:
    try:
        return session.query(model).filter_by(**unique_kwargs).one(), False
    except NoResultFound:
        params = _extract_model_params(defaults, **unique_kwargs)
        return _create_object_from_params(session, model, unique_kwargs, params)


def update_or_create(
    session: Session,
    model: DeclarativeBase,
    defaults: dict | None = None,
    **unique_kwargs
) -> tuple[DeclarativeMeta, bool]:
    defaults = defaults or {}
    try:
        obj = session.query(model).with_for_update().filter_by(**unique_kwargs).one()
    except NoResultFound:
        params = _extract_model_params(defaults, **unique_kwargs)
        obj, created = _create_object_from_params(session, model, unique_kwargs, params)

        if created:
            return obj, True

    for k, v in defaults.items():
        setattr(obj, k, v)

    session.add(obj)

    return obj, False
