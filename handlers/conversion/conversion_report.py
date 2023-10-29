from loader import bot, conversion_states
from keyboards.inline.conversion_months import get_months_markup

from telebot.types import Message


@bot.message_handler(commands=['conversion'])
def handle_conversion_command(message: Message):
    id = message.chat.id
    bot.send_message(id, 'Выбери месяц', reply_markup=get_months_markup())
    bot.set_state(id, state=conversion_states.choose_month)
