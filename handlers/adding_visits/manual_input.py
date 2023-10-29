from loader import bot, states
from utils.procedures import add_procedure

from telebot.types import Message


@bot.message_handler(state=states.manual_input, is_positive_and_zero_digit=True)
def manual_input_handler(message: Message):
    id = message.chat.id
    manual_value = int(message.text)

    bot.add_data(id, manual_value=manual_value)

    add_procedure(id)


@bot.message_handler(state=states.manual_input, is_positive_and_zero_digit=False)
def manual_input_wrong_value_handler(message: Message):
    bot.send_message(
        message.chat.id,
        'Нужно ввести положительное число либо 0!'
    )
