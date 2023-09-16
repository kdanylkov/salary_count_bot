from loader import Session
from .core import get_or_create
from database.models.user import UserModel


def fetch_user_by_telegram_id(telegram_id: int):
    ...


def get_or_create_user(telegram_id: int, name: str):
    with Session.begin() as session:
        user, created = get_or_create(session, UserModel, id=telegram_id, name=name)

    return user
