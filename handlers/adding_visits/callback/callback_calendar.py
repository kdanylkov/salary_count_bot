from telebot.types import CallbackQuery, ReplyKeyboardRemove, Message

from datetime import datetime

from loader import bot, calendar_1_callback, calendar, states
from config import TIMEZONE
from utils.calendar import get_calendar
from data.objects import Workday


@bot.callback_query_handler(
    state=states.choose_date,
    func=lambda c: c.data.startswith(calendar_1_callback.prefix),
)
def date_chosen(call: CallbackQuery):
    id = call.message.chat.id
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
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

            bot.send_message(id, text, reply_markup=get_calendar(now))
        else:
            if action == "DAY":
                text = f'Ты выбрала дату: {date.strftime("%d.%m.%Y")}'
                bot.send_message(id, text)
                bot.set_state(id, states.client_name)

                bot.add_data(id, date=date)

                text = "Введи имя клиента"
                bot.send_message(id, text=text)


@bot.message_handler(state=states.choose_date, content_types=["text"])
def date_choice_keyboard_input(message: Message):
    t = "Нажми на одну из кнопок⬆️ "
    bot.send_message(message.chat.id, t)
