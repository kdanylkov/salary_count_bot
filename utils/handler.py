from telebot import TeleBot
from telebot.types import ReplyKeyboardRemove


def cancel_action(chat_id: int, bot: TeleBot) -> None:
    text = "Операция отменена."
    bot.send_message(chat_id, text, reply_markup=ReplyKeyboardRemove())
    bot.delete_state(chat_id)
