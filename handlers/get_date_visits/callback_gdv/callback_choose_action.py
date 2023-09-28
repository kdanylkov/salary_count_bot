from loader import bot, show_date_states, states, calendar_2_callback
from keyboards.inline.choose_visit import choose_visit
from exceptions.handlers import UnknownCallbackError
from utils.calendar import get_calendar
from config import TIMEZONE

from telebot.types import CallbackQuery, Message
from datetime import datetime


@bot.callback_query_handler(func=lambda c: c.data.startswith("action:"))
def callback_choose_action(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    if call.data.endswith("idle_time"):
        bot.send_message(
            id, "Введи новое значение времени (в минутах):"
        )
        bot.set_state(id, show_date_states.idle_hours)
    elif call.data.endswith("delete"):
        text = "Выбери посещение"
        workday = bot.retrieve_data(id).data["workday"]
        bot.send_message(id, text, reply_markup=choose_visit(workday))
        bot.set_state(id, show_date_states.choose_visit)
    elif call.data.endswith("add_another"):
        bot.set_state(id, states.client_name)
        bot.send_message(id, "Введи имя клиента:")
    elif call.data.endswith("another_date"):
        bot.set_state(id, show_date_states.choose_date)
        now = TIMEZONE.localize(datetime.now())
        text = "Выбери дату"

        bot.send_message(id, text, reply_markup=get_calendar(now, calendar_2_callback))
    else:
        raise UnknownCallbackError(call.data)


@bot.message_handler(state=show_date_states.choose_action, content_types=["text"])
def handler_choose_action_keyboard_input(message: Message):
    bot.send_message(message.chat.id, "Нажми на одну из кнопок⬆️")
