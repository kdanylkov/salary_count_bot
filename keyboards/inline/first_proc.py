from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def if_first():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton(callback_data="first_yes", text="Да")
    btn2 = InlineKeyboardButton(callback_data="first_no", text="Нет")

    markup.add(btn1, btn2)

    return markup
