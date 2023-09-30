from loader import bot, states, show_date_states
from exceptions.handlers import UnknownCallbackError
from exceptions.objects import VisitNotDeleted, ProcedureNotDeleted
from data.objects import Visit, Workday
from utils.visit import delete_visit
from utils.procedures import delete_procedure
from keyboards.inline.choose_date_action import choose_action

from telebot.types import CallbackQuery
from re import search


@bot.callback_query_handler(func=lambda c: c.data.startswith('choose_proc'))
def callback_choose_proc(call: CallbackQuery):
    id = call.message.chat.id
    suffix = call.data[-3:]
    bot.delete_message(id, call.message.id)

    res = search(r'\d+', call.data)
    if res is None:
        raise UnknownCallbackError(call.data)
    proc_id = int(res.group(0))

    visit: Visit = bot.retrieve_data(id).data['workday_visit']

    if suffix == 'del':
        if len(visit.procedures) == 1:
            try:
                delete_visit(bot, id)
            except VisitNotDeleted:
                bot.send_message(
                    id, 'Произошла ошибка. Сообщи в службу поддержки.')
                raise
            else:
                _send_message_after_deletion(
                        "Посещение удалено,"
                        "т.к. удалена последняя процедура в посещении.\n",
                        id)
        else:
            try:
                delete_procedure(bot, id, proc_id)
            except ProcedureNotDeleted:
                bot.send_message(
                    id, 'Произошла ошибка. Сообщи в службу поддержки.')
                raise
            else:
                _send_message_after_deletion("Процедура успешено удалена.", id)


def _send_message_after_deletion(message: str, chat_id) -> None:
    workday: Workday = bot.retrieve_data(chat_id).data['workday']
    message += workday.workday_report()

    bot.send_message(chat_id, message,
                     reply_markup=choose_action(workday.visits))
    bot.set_state(chat_id, show_date_states.choose_action)
