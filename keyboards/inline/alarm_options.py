from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup


def alarm_on_off(alarm_on: bool) -> InlineKeyboardMarkup:
    text = 'Выключить' if alarm_on else 'Включить'
    return quick_markup(
        {
            text: {"callback_data": "alarm_switch"},
            "Отмена": {"callback_data": "alarm_cancel"},
        },
        row_width=2,
    )
