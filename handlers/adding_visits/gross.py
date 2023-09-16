from loader import bot, states
from utils.procedures import add_procedure

from telebot.types import Message


@bot.message_handler(
    state=states.choose_gross, content_types=["text"], is_positive_digit=True
)
def gross_amount_handler(message: Message):
    gross = int(message.text)
    text = "Введена сумма: {}".format(gross)
    bot.send_message(message.chat.id, text)
    bot.add_data(message.chat.id, gross=gross)

    add_procedure(message.chat.id)


@bot.message_handler(
    state=states.choose_gross, content_types=["text"], is_positive_digit=False
)
def gross_amount_handler_incorrect(message: Message):
    text = "Сумма должна быть числом больше нуля!"
    bot.send_message(message.chat.id, text)
