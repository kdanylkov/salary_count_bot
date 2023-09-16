from loader import bot

from telebot.types import Message


@bot.message_handler(state=None)
def undefined(message: Message) -> None:
    text = 'Я тебя не понимаю😢. Напиши "/help"'
    bot.reply_to(message, text=text)
