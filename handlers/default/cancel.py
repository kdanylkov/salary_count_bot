from loader import bot

from telebot.types import Message


@bot.message_handler(commands=["cancel"])
def cancel_handler(message: Message):
    bot.delete_state(message.from_user.id, message.chat.id)

    text = """
Отмена операции прошла успешно.
Можешь воспользоваться одной из команд.
Для вызова подсказки нажми /help
    """
    bot.send_message(message.chat.id, text=text)
