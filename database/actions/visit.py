from __future__ import annotations

from database.actions.workday import get_or_create_workday
from database.models import VisitModel, WorkDayModel
from database.actions.procedures import get_procedure_for_db
from loader import Session

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import and_

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.objects import Visit


def create_visit_with_procedures(data: dict, user_id: int, date: datetime) -> None:
    """
    Create a visit with associated procedures in the database.

    Args:
        data (dict): Data containing information about the visit and procedures.
        user_id (int): ID of the user associated with the visit.
        date (datetime): Date of the visit.

    Returns:
        None
    """
    with Session() as session:
        # Get or create the workday for the user and date
        workday = get_or_create_workday(session, user_id, date)

        # Extract data from the input dictionary
        visit_time = data["visit_time"]
        laser_conversion_status = data["laser_conversion_status"]

        # Create the VisitModel object
        visit = VisitModel(
            visit_time=visit_time,
            workday=workday,
            user_id=user_id,
            laser_conversion_status=laser_conversion_status
        )

        # Process and add the procedures to the visit
        procedures = data.get("procedures", [])
        for entry in procedures:
            proc = get_procedure_for_db(entry)
            visit.procedures.append(proc)

        # Add the visit to the session and commit the changes
        session.add(visit)
        session.commit()


def delete_visit_from_db(id: int) -> bool:
    """
    Delete a visit from the database.

    Args:
        id (int): ID of the visit to be deleted.

    Returns:
        bool: True if the visit was successfully deleted, False otherwise.
    """
    with Session() as session:
        try:
            # Get the visit by ID
            visit = session.query(VisitModel).get(id)
            if visit:
                # Delete the visit and commit the changes
                session.delete(visit)
                session.commit()
                return True
            else:
                return False
        except NoResultFound:
            return False


def calculate_conversion_rate(user_id: int,
                              start_date: datetime,
                              end_date: datetime) -> int:
    with Session.begin() as session:

        total_new_clients, new_clients_bought = session.query(
            func.count(VisitModel.user_id),
            func.count(func.nullif(
                VisitModel.laser_conversion_status != 'NEW_BOUGHT', True))
        ).filter(
            VisitModel.user_id == user_id,
            VisitModel.workday.has(
                WorkDayModel.date.between(start_date, end_date)),
            VisitModel.laser_conversion_status.in_(
                ['NEW_BOUGHT', 'NEW_NOT_BOUGHT'])
        ).first()

        if total_new_clients > 0:
            conversion_rate = (new_clients_bought / total_new_clients) * 100
        else:
            conversion_rate = 0

        return int(conversion_rate), total_new_clients, new_clients_bought


def get_visits_new_clients_by_period(user_id: int,
                                     start_date: datetime,
                                     end_date: datetime) -> list[Visit]:
    from utils.visit import create_visit_from_db_model

    with Session.begin() as session:
        stmt = select(VisitModel).join(VisitModel.workday).filter(
            VisitModel.user_id == user_id,
            VisitModel.workday.has(
                WorkDayModel.date.between(start_date, end_date)
            ),
            VisitModel.laser_conversion_status.in_(
                ['NEW_BOUGHT', 'NEW_NOT_BOUGHT']
            )
        ).order_by(WorkDayModel.date)

        result = session.execute(stmt)
        visits = [
            create_visit_from_db_model(visit) for visit in result.scalars()
        ]
        return visits
