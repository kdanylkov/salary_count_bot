from __future__ import annotations

from database.actions.visit import delete_visit_from_db
from exceptions.objects import VisitNotDeleted
from config import PROCEDURE_PARAMS

from telebot import TeleBot
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models import VisitModel
    from data.objects import Workday


def delete_visit(bot: TeleBot, id: str | int) -> None:
    visit = bot.retrieve_data(id).data["visit"]
    workday: Workday = bot.retrieve_data(id).data['workday']

    deleted_from_db = delete_visit_from_db(visit.db_id)
    deleted_from_obj = workday.delete_visit(visit.db_id)

    if not delete_visit_from_db or not deleted_from_obj:
        raise VisitNotDeleted(deleted_from_db, deleted_from_obj)
    bot.add_data(id, workday=workday)


def clean_state(bot, id):
    with bot.retrieve_data(id) as data:
        to_delete = PROCEDURE_PARAMS + ['for_deletion', 'edit_visit']
        for key in to_delete:
            if key in data:
                data.pop(key)


def create_visit_from_db_model(visit: VisitModel):
    from data.objects import Visit

    data = visit.as_dict()
    procs = data.pop("procedures")
    visit = Visit(**data)

    for proc in procs:  # type: dict
        if proc["type"] == "LASER" and proc.get("subscriptions"):
            subscriptions = proc.pop("subscriptions")
            visit.procedures.add(**proc)
            for sub in subscriptions:
                visit.procedures.add_laser_sub(**sub)
        else:
            visit.procedures.add(**proc)
    return visit
