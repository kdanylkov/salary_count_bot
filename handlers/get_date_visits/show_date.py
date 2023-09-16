from loader import bot, calendar_2_callback, show_date_states
from config import TIMEZONE
from utils.calendar import get_calendar

from telebot.types import Message
from datetime import datetime


@bot.message_handler(commands=["show_date"])
def show_day_handler(message: Message):
    bot.set_state(message.chat.id, show_date_states.choose_date)
    now = TIMEZONE.localize(datetime.now())
    text = "Выбери дату"

    bot.send_message(
        message.chat.id, text, reply_markup=get_calendar(now, calendar_2_callback)
    )
