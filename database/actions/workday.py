from database.actions.core import get_or_create, update_or_create
from database.models import WorkDayModel
from database.models import VisitModel
from database.models import ProcedureModel
from data.objects import Visit, Workday
from loader import Session
from utils.dates import range_of_dates

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def get_or_create_workday(session, user_id: int, date: datetime):
    workday, _ = get_or_create(
        session, WorkDayModel, user_id=user_id, date=date)

    return workday


def get_workday_with_visits_from_db(
    user_id: int, date: datetime
) -> list[dict[tuple, Visit]] | None:
    with Session.begin() as session:
        workday = get_or_create_workday(session, user_id, date)

        stmt = (
            select(VisitModel)
            .options(selectinload(VisitModel.procedures)
                     .selectinload(ProcedureModel.subscriptions))
            .where(VisitModel.workday == workday).
            order_by(VisitModel.client_name)
        )

        db_visits = session.scalars(stmt).all()

        if not len(db_visits):
            return Workday(date=date, idle_time=workday.idle_time)

        workday = Workday(
            date=workday.date, visits=db_visits, idle_time=workday.idle_time
        )

        return workday


def update_idle_hours(
    id: int, date: datetime, idle_hours: int, workday: Workday
) -> Workday:
    with Session.begin() as session:
        db_workday, created = update_or_create(
            session, WorkDayModel, {"idle_time": idle_hours}, user_id=id, date=date
        )
        workday.idle_time = db_workday.idle_time
    return workday


def get_workdays_for_period(
    user_id: int, start_date: datetime, end_date: datetime
) -> list[Workday]:
    workdays = []
    for date in range_of_dates(start_date, end_date):
        workday = get_workday_with_visits_from_db(user_id, date)
        if not workday.idle_time and not workday.visits:
            continue
        workdays.append(workday)

    return workdays
