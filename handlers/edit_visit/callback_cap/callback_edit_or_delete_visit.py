from loader import bot, show_date_states, states
from data.objects import Visit, Workday
from keyboards.inline.choose_date_action import choose_action
from keyboards.inline.choose_proc_to_change import choose_proc
from keyboards.inline.treatment_types import types_keyboard
from exceptions.handlers import UnknownCallbackError
from exceptions.objects import VisitNotDeleted
from utils.visit import delete_visit

from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda c: c.data.startswith("edit_visit"))
def callback_edit_or_delete_visit(call: CallbackQuery):
    suffix = call.data[call.data.index(':') + 1:]
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    if suffix == 'del_visit':
        try:
            delete_visit(bot, id)
        except VisitNotDeleted:
            bot.send_message(
                id, "Что-то пошло не так... Обратись в службу поддержки.")
        else:
            workday: Workday = bot.retrieve_data(id).data['workday']
            text = 'Посещение удалено!\n' + workday.workday_report()
            bot.send_message(id,
                             text,
                             reply_markup=choose_action(workday.visits))
            bot.set_state(id, show_date_states.choose_action)

    elif suffix in ['chg_proc', 'del_proc']:
        prefix = suffix[:3]
        visit: Visit = bot.retrieve_data(id).data["visit"]

        text = visit.visit_report() + '\nВыбери процедуру:'
        bot.send_message(id, text, reply_markup=choose_proc(visit, prefix))
        bot.set_state(id, state=show_date_states.choose_proc)

    elif suffix == 'add_proc':
        bot.add_data(id, edit_visit=True)
        bot.set_state(id, states.choose_type)

        bot.send_message(id, 'Выбери тип процедуры',
                         reply_markup=types_keyboard())

    elif suffix == 'cancel':
        bot.delete_state(id)
        bot.send_message(id, "Операция отменена.")

    else:
        raise UnknownCallbackError(call.data)
