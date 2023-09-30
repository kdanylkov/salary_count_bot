from sqlalchemy.exc import NoResultFound, IntegrityError

from database.models import ProcedureModel
from loader import Session


def delete_procedure_from_db(proc_id: int) -> bool:
    with Session() as session:
        try:
            procedure = session.get(ProcedureModel, proc_id)
            session.delete(procedure)
            return True
        except (NoResultFound, IntegrityError):
            return False
        finally:
            session.commit()
