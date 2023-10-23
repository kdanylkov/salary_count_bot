from loader import bot, states
from utils.calendar import get_calendar

from telebot.types import Message

from datetime import datetime


@bot.message_handler(commands=["add_visit"])
def choose_treatment_date(message: Message):
    bot.set_state(message.from_user.id, states.choose_date, message.chat.id)

    now = datetime.now()
    text = "Выбери дату посещения"

    bot.send_message(message.chat.id, text, reply_markup=get_calendar(now))
