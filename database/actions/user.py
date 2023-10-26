from loader import Session
from .core import get_or_create
from database.models.user import UserModel


def get_or_create_user(telegram_id: int, name: str):
    with Session.begin() as session:
        user, created = get_or_create(session, UserModel, id=telegram_id, name=name)

    return user


def get_user_alarm_status(user_id: str) -> bool:
    with Session.begin() as session:
        user = session.get(UserModel, user_id)
        return user.alarm_on


def switch_alarm_status(user_id: int):
    with Session.begin() as session:
        user: UserModel = session.get(UserModel, user_id)
        user.alarm_on = not user.alarm_on
