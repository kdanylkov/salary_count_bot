from sqlalchemy.exc import NoResultFound, IntegrityError
from datetime import datetime

from database.models import ProcedureModel
from database.models import SubscriptionModel
from database.models import VisitModel
from loader import Session


def delete_procedure_from_db(proc_id: int) -> bool:
    with Session() as session:
        try:
            procedure = session.get(ProcedureModel, proc_id)
            session.delete(procedure)
        except (NoResultFound, IntegrityError):
            return False
        else:
            return True
        finally:
            session.commit()


def get_procedure_for_db(data: dict):
    subs = data.get("subscriptions")

    if subs:
        subs = data.pop("subscriptions")
        proc = ProcedureModel(**data)
        for sub in subs:
            subscription = SubscriptionModel(**sub)
            proc.subscriptions.append(subscription)
    else:
        proc = ProcedureModel(**data)

    return proc


def create_procedure_in_db(visit_id: int, proc_data: dict):
    with Session() as session:
        try:
            visit = session.get(VisitModel, visit_id)
            proc = get_procedure_for_db(proc_data)
            visit.procedures.append(proc)
        except (IntegrityError, NoResultFound):
            return False
        else:
            return True
        finally:
            session.commit()
