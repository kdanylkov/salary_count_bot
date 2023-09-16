from loader import (
    bot,
    period_states,
    calendar,
    calendar_3_callback,
    calendar_4_callback,
)
from config import TIMEZONE
from utils.calendar import get_calendar

from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from datetime import datetime


@bot.callback_query_handler(
    func=lambda c: c.data.startswith(calendar_3_callback.prefix)
)
def date_chosen(call: CallbackQuery):
    id = call.message.chat.id
    name, action, year, month, day = call.data.split(calendar_3_callback.sep)
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "CANCEL":
        text = "Операция отменена."
        bot.send_message(id, text, reply_markup=ReplyKeyboardRemove())
        bot.delete_state(id)

    else:
        date = TIMEZONE.localize(date)
        now = TIMEZONE.localize(datetime.now())
        if date > now:
            text = "Дату в будущем нельзя выбирать!"

            bot.send_message(
                id, text, reply_markup=get_calendar(now, calendar_3_callback)
            )
        else:
            if action == "DAY":
                text = f'Ты выбрала дату: {date.strftime("%d.%m.%Y")}'
                bot.send_message(id, text)
                bot.set_state(id, period_states.get_end_date)

                bot.add_data(id, start_date=date)

                text = "Введи конечную дату:"
                bot.send_message(
                    id, text=text, reply_markup=get_calendar(now, calendar_4_callback)
                )


@bot.message_handler(state=period_states.get_start_date, content_types=["text"])
def handler_period_start_date_keyboard_input(message: Message):
    t = "Нажми на одну из кнопок⬆️ "
    bot.send_message(message.chat.id, t)
