from database.actions.workday import get_or_create_workday
from database.models import VisitModel
from database.actions.procedures import get_procedure_for_db
from loader import Session

from datetime import datetime
from sqlalchemy.exc import NoResultFound, IntegrityError


def create_visit_with_procedures(data: dict, user_id, date: datetime):
    with Session.begin() as session:
        workday = get_or_create_workday(session, user_id, date)
        client_name = data["client_name"]
        laser_conversion_status = data["laser_conversion_status"]

        visit = VisitModel(
            client_name=client_name, workday=workday,
            user_id=user_id, laser_conversion_status=laser_conversion_status
        )

        procedures = data["procedures"]
        for entry in procedures:  # type: dict
            proc = get_procedure_for_db(entry)
            visit.procedures.append(proc)

        session.add(visit)


def delete_visit_from_db(id: int) -> bool:
    with Session() as session:
        try:
            visit = session.get(VisitModel, id)
            session.delete(visit)
            return True
        except (NoResultFound, IntegrityError):
            return False
        finally:
            session.commit()
