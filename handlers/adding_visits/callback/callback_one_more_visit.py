from keyboards.inline.proc_time import get_times_makrup
from loader import bot, states, show_date_states
from data.objects import Workday
from database.actions.workday import get_workday_with_visits_from_db
from keyboards.inline.choose_date_action import choose_action
from utils.handler import cancel_action

from telebot.types import CallbackQuery, Message
from datetime import datetime


@bot.callback_query_handler(func=lambda c: c.data.startswith("one_more_visit"))
def callback_one_more_visit(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    if call.data.endswith("yes"):
        bot.set_state(id, states.visit_time)
        text = "Выбери время посещения"
        bot.send_message(id, text=text, reply_markup=get_times_makrup())
    elif call.data.endswith("cancel"):
        cancel_action(id, bot)
    elif call.data.endswith("overview"):
        date: datetime = bot.retrieve_data(id).data.get("date")
        workday: Workday = get_workday_with_visits_from_db(id, date)
        bot.add_data(id, workday=workday)

        text = workday.workday_report()
        bot.send_message(id, text, reply_markup=choose_action(workday.visits))
        bot.set_state(id, show_date_states.choose_action)


@bot.message_handler(state=states.if_one_more_visit, content_types=["text"])
def if_one_more_visit_keyboard_input(message: Message):
    t = "Нажми на одну из кнопок⬆️"
    bot.send_message(message.chat.id, t)
