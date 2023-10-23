from loader import bot
from database.actions.user import get_or_create_user

from telebot.types import Message


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):

    get_or_create_user(message.from_user.id, message.from_user.first_name)
    name = message.from_user.first_name
    message_to_user = """
Привет, {name}!
Меня зовут SalaryCountBot.
Я бот для расчета твоей зарплаты за определённый период.
Для вызова справки нажми /help
    """.format(
        name=name
    )

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, message_to_user)
