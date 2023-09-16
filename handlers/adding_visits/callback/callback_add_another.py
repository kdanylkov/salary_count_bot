from loader import bot, states
from exceptions.handlers import UnknownCallbackError
from keyboards.inline.treatment_types import types_keyboard
from keyboards.inline.if_one_more_visit import one_more_visit
from data.objects import Visit
from config import PROCEDURE_PARAMS
from database.actions.visit import create_visit_with_procedures

from telebot.types import CallbackQuery, Message


@bot.callback_query_handler(func=lambda c: c.data.startswith("another"))
def add_another(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)
    _clean_state(id)

    if call.message:
        if call.data == "another_yes":
            bot.set_state(id, states.choose_type)
            bot.send_message(id, "Выбери тип процедуры:", reply_markup=types_keyboard())
        elif call.data == "another_no":
            with bot.retrieve_data(id) as data:
                visit: Visit = data["visit"]
                date = data["date"]

                create_visit_with_procedures(visit.to_dict(), int(id), date)

            report = visit.visit_report()
            bot.send_message(id, report, reply_markup=one_more_visit())
            bot.set_state(id, states.if_one_more_visit)
        else:
            bot.send_message(id, "Ошибка! Обратись в службу поддержки.")
            raise UnknownCallbackError(call.data)


@bot.message_handler(state=states.if_add_another, content_types=["text"])
def add_another_keyboard_input(message: Message):
    bot.send_message(message.chat.id, 'Нажми на кнопку "Да" или "Нет"⬆️')


def _clean_state(id):
    with bot.retrieve_data(id) as data:
        for key in PROCEDURE_PARAMS:
            if key in data:
                data.pop(key)
