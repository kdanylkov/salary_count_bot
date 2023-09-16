from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def if_subscription():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton(callback_data="subscription_yes", text="Да")
    btn2 = InlineKeyboardButton(callback_data="subscription_no", text="Нет")

    markup.add(btn1, btn2)

    return markup
