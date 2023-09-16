from loader import bot, states
from config import TIMEZONE
from utils.calendar import get_calendar
from database.actions.user import get_or_create_user

from telebot.types import Message

from datetime import datetime


@bot.message_handler(commands=["add_visit"])
def choose_treatment_date(message: Message):
    bot.set_state(message.from_user.id, states.choose_date, message.chat.id)

    get_or_create_user(message.from_user.id, message.from_user.first_name)

    now = TIMEZONE.localize(datetime.now())
    text = "Выбери дату посещения"

    bot.send_message(message.chat.id, text, reply_markup=get_calendar(now))
