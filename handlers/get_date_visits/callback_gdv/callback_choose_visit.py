from loader import bot, show_date_states
from keyboards.inline.change_delete_visit import edit_visit
from data.objects import Workday

from telebot.types import CallbackQuery
import json


@bot.callback_query_handler(func=lambda c: c.data.startswith('{"choose_visit"'))
def callback_choose_visit(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    try:
        workday = bot.retrieve_data(id).data["workday"]
    except KeyError:
        bot.send_message(id, "Произошла ошибка. Обратитесь в службу поддержки")
        bot.delete_state(id)
    else:
        visit_db_id = int(json.loads(call.data)["choose_visit"])

        visit = _get_visit_by_id(visit_db_id, workday)
        if visit is None:
            print("Error: Could not get a visit by db_id")
            bot.send_message(id, "Произошла ошибка. Обратитесь в службу поддержки")
            bot.delete_state(id)
        else:
            bot.add_data(id, workday_visit=visit)
            bot.send_message(id, visit.visit_report(),
                             reply_markup=edit_visit())

            bot.set_state(id, state=show_date_states.if_change_delete_visit)


@bot.message_handler(state=show_date_states.choose_visit, content_types=["text"])
def callback_choose_visit_keyboard_input(message):
    t = 'Нажми на одну из кнопок⬆️\
(или выбери пункт меню "Отменить текущую операцию")'
    bot.send_message(message.chat.id, t)


def _get_visit_by_id(id: int, workday: Workday):
    for v in workday.visits:
        if v.db_id == id:
            return v
    return None
