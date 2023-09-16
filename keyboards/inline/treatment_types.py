from data.types import TreatemtTypes

from telebot.util import quick_markup


def types_keyboard():
    return quick_markup(
        {type.value: {"callback_data": type.name} for type in TreatemtTypes},
        row_width=2,
    )
