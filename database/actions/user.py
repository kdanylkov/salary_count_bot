from loader import Session
from .core import get_or_create
from database.models.user import UserModel

from sqlalchemy import select


def get_or_create_user(telegram_id: int, name: str):
    with Session.begin() as session:
        user, created = get_or_create(
            session, UserModel, id=telegram_id, name=name)

    return user


def get_user_alarm_status(user_id: str) -> bool:
    with Session.begin() as session:
        user = session.get(UserModel, user_id)
        return user.alarm_on


def switch_alarm_status(user_id: int):
    with Session.begin() as session:
        user: UserModel = session.get(UserModel, user_id)
        user.alarm_on = not user.alarm_on


def get_users_ids_with_alarm_on():
    with Session.begin() as session:
        result = session.execute(
            select(UserModel).where(UserModel.alarm_on == True)
        )
        ids = [user.id for user in result.scalars()]
        print(ids)
        return ids
