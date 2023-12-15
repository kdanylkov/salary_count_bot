from __future__ import annotations

from database.actions.visit import delete_visit_from_db, change_visit_time_in_db
from exceptions.objects import VisitNotDeleted
from config import PROCEDURE_PARAMS
from keyboards.inline.choose_date_action import choose_action
from loader import show_date_states

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
        to_delete = PROCEDURE_PARAMS + ['for_deletion', 'edit_visit', 'visit_to_change_time_id']
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


def change_visit_time(bot: TeleBot, mes_id: int, visit_id: int, new_time_value: str) -> None:
    success = change_visit_time_in_db(visit_id, new_time_value)
    if success:
        from database.actions.workday import get_workday_with_visits_from_db

        with bot.retrieve_data(mes_id) as data:
            workday = get_workday_with_visits_from_db(mes_id, data.get('date'))
            data['workday'] = workday

        text = '\n'.join(['ВРЕМЯ ПОСЕЩЕНИЯ БЫЛО ИЗМЕНЕНО!', workday.workday_report()])

        bot.set_state(mes_id, state=show_date_states.choose_action)
        bot.send_message(mes_id, text, reply_markup=choose_action(workday.visits))
    else:
        bot.send_message(mes_id, 'Произошла ошибка! Обратись в службу поддержки!')
    clean_state(bot, mes_id)
