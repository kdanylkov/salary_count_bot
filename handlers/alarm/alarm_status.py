from loader import bot
from database.actions.user import get_user_alarm_status
from keyboards.inline.alarm_options import alarm_on_off

from telebot.types import Message


@bot.message_handler(commands=['alarm'])
def handle_alarm_status(message: Message):
    id = message.chat.id

    alarm_on: bool = get_user_alarm_status(id)

    status = 'Включены' if alarm_on else 'Отключены'

    text = f'Напоминания <b>{status.upper()}</b>'
    bot.send_message(id, text, reply_markup=alarm_on_off(alarm_on))
