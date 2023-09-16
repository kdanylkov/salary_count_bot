from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def if_add_another():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton(callback_data="another_yes", text="Да")
    btn2 = InlineKeyboardButton(callback_data="another_no", text="Нет")

    markup.add(btn1, btn2)

    return markup
