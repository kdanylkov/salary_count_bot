from loader import bot

from telebot.types import Message


@bot.message_handler(commands=["start", "help"])
def send_welcome(message: Message):
    name = message.from_user.first_name
    message_to_user = """
Привет, {name}!
Меня зовут SalaryCountBot.
Я бот для расчета твоей зарплаты за определённый период.
    """.format(
        name=name
    )

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, message_to_user)
