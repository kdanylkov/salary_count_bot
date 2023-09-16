from loader import bot, show_date_states
from data.objects import Workday
from database.actions.workday import update_idle_hours
from database.actions.workday import get_workday_with_visits_from_db
from keyboards.inline.choose_date_action import choose_action

from telebot.types import Message
from datetime import datetime


@bot.message_handler(state=show_date_states.idle_hours, is_positive_digit=True)
def idle_hours_handler(message: Message):
    id = message.chat.id
    idle_hours = int(message.text)

    workday: Workday = bot.retrieve_data(id).data.get("workday")
    date: datetime = bot.retrieve_data(id).data.get("date")
    if workday is None:
        workday = get_workday_with_visits_from_db(id, date)

    updated_workday = update_idle_hours(
        id=id, workday=workday, idle_hours=idle_hours, date=date
    )
    bot.add_data(id, workday=updated_workday)

    text = updated_workday.workday_report()
    text = "<b>ДАННЫЕ ОБНОВЛЕНЫ</b>\n" + text

    bot.set_state(id, show_date_states.choose_action)
    bot.send_message(id, text, reply_markup=choose_action(updated_workday.visits))
