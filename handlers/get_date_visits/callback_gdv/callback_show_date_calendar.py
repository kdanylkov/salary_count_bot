from telebot.types import CallbackQuery, Message
from datetime import datetime

from loader import bot, calendar_2_callback, calendar, show_date_states
from utils.calendar import get_calendar
from utils.handler import cancel_action
from database.actions.workday import get_workday_with_visits_from_db
from keyboards.inline.choose_date_action import choose_action
from data.objects import Workday


@bot.callback_query_handler(
    func=lambda c: c.data.startswith(calendar_2_callback.prefix)
)
def show_date_visits_calendar(call: CallbackQuery):
    id = call.message.chat.id
    name, action, year, month, day = call.data.split(calendar_2_callback.sep)
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "CANCEL":
        cancel_action(id, bot)

    elif action == "DAY":
        date = date
        now = datetime.now()
        if date > now:
            text = "Дату в будущем нельзя выбирать!"

            bot.send_message(
                id, text, reply_markup=get_calendar(now, calendar_2_callback)
            )
        else:
            text = f'Ты выбрала дату: {date.strftime("%d.%m.%Y")}'

            bot.send_message(id, text)
            workday: Workday = get_workday_with_visits_from_db(id, date)

            bot.set_state(id, show_date_states.choose_action)
            text = workday.workday_report()

            bot.add_data(id, workday=workday, date=date)
            bot.send_message(id, text, reply_markup=(choose_action(workday.visits)))


@bot.message_handler(state=show_date_states.choose_date, content_types=["text"])
def date_choice_keyboard_input(message: Message):
    text = "Нужно нажать одну из кнопок!⬆️"
    bot.send_message(message.chat.id, text=text)
