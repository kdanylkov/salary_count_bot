from loader import bot, period_states
from exceptions.handlers import UnknownCallbackError
from utils.create_file import send_report, get_file_instance
from data.objects import PeriodReport

from telebot.types import CallbackQuery, Message


@bot.callback_query_handler(func=lambda c: c.data.startswith("full_report"))
def callback_if_full_report(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    if call.data.endswith("yes"):
        period: PeriodReport = bot.retrieve_data(id).data.get("period")
        send_report(period, bot, id)
    elif call.data.endswith("cancel"):
        bot.delete_state(id)
        bot.send_message(id, "Отмена операции")
    else:
        raise UnknownCallbackError(call.data)


@bot.message_handler(state=period_states.get_full_report, content_types=["text"])
def callback_if_full_report_keyboard_input(message: Message):
    t = "Нажми на одну из кнопок⬆️ "
    bot.send_message(message.chat.id, t)
