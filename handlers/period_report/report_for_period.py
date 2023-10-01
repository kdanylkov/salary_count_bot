from loader import bot, period_states, calendar_3_callback
from utils.calendar import get_calendar

from telebot.types import Message
from datetime import datetime


@bot.message_handler(commands=["report"])
def handler_report_for_period(message: Message):
    id = message.chat.id
    now = datetime.now()
    bot.set_state(id, period_states.get_start_date)
    bot.send_message(
        id,
        "Выбери начальную дату:",
        reply_markup=get_calendar(now, calendar_3_callback),
    )
