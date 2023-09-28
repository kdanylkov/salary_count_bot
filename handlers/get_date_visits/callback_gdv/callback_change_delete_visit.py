from loader import bot, show_date_states
from database.actions.visit import delete_visit_from_db
from data.objects import Workday
from keyboards.inline.choose_date_action import choose_action
from exceptions.handlers import UnknownCallbackError
from exceptions.objects import VisitNotDeleted

from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda c: c.data.startswith("chan_del"))
def callback_if_delete_visit(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)
    if call.data.endswith("delete"):
        visit = bot.retrieve_data(id).data["workday_visit"]
        workday: Workday = bot.retrieve_data(id).data['workday']

        deleted_from_db = delete_visit_from_db(visit.db_id)
        deleted_from_obj = workday.delete_visit(visit.db_id)

        bot.add_data(id, workday=workday)

        if deleted_from_db and deleted_from_obj:
            text = 'Посещение удалено!\n' + workday.workday_report()
            bot.send_message(id,
                             text,
                             reply_markup=choose_action(workday.visits))
            bot.set_state(id, show_date_states.choose_action)

        else:
            bot.send_message(
                id, "Что-то пошло не так... Обратись в службу поддержки.")
            raise VisitNotDeleted(deleted_from_db, deleted_from_obj)
    elif call.data.endswith("change"):
        bot.send_message(id, 'Works')
    elif call.data.endswith("cancel"):
        bot.delete_state(id)
        bot.send_message(id, "Операция отменена.")
    else:
        raise UnknownCallbackError(call.data)
