from database.actions.workday import get_or_create_workday
from database.models import VisitModel
from database.models import SubscriptionModel
from database.models import ProcedureModel
from loader import Session

from datetime import datetime
from sqlalchemy.exc import NoResultFound, IntegrityError


def create_visit_with_procedures(data: dict, user_id, date: datetime):
    with Session.begin() as session:
        workday = get_or_create_workday(session, user_id, date)

        visit = VisitModel(
            client_name=data["client_name"], workday=workday, user_id=user_id
        )

        procedures = data["procedures"]
        for entry in procedures:  # type: dict
            subs = entry.get("subscriptions")

            if subs:
                subs = entry.pop("subscriptions")
                proc = ProcedureModel(**entry)
                for sub in subs:
                    subscription = SubscriptionModel(**sub)
                    proc.subscriptions.append(subscription)
            else:
                proc = ProcedureModel(**entry)

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
