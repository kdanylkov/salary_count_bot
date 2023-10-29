from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

from config import MONTH_MAPPING


def get_months_markup() -> InlineKeyboardMarkup:
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    keyboard = InlineKeyboardMarkup()

    buttons = []

    for i in range(4):
        month = current_month - i
        year = current_year

        if month < 1:
            month += 12
            year -= 1

        month_str = MONTH_MAPPING[datetime.date(1900, month, 1).strftime("%B")]
        year_str = str(year)

        button = InlineKeyboardButton(
            text=f"{month_str} {year_str}",
            callback_data=f"month_of_conversion_{month}_{year}"
        )
        buttons.append(button)

    keyboard.row(*buttons[:2])
    keyboard.row(*buttons[2:])

    return keyboard
