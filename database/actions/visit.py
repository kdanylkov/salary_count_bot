from database.actions.workday import get_or_create_workday
from database.models import VisitModel
from database.actions.procedures import get_procedure_for_db
from loader import Session

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound


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
        client_name = data["client_name"]
        laser_conversion_status = data["laser_conversion_status"]

        # Create the VisitModel object
        visit = VisitModel(
            client_name=client_name,
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
