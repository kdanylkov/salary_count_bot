from telebot.util import quick_markup
from telebot.types import InlineKeyboardButton


def choose_action(visits):
    markup = quick_markup(
        {
            "Время": {"callback_data": "action:idle_time"},
            "Добавить посещение": {"callback_data": "action:add_another"},
        },
        row_width=1,
    )

    if visits:
        btn = InlineKeyboardButton(
            text="Изменить/Удалить посещение", callback_data="action:ch_or_del"
        )
        markup.add(btn)
    markup.add(
        InlineKeyboardButton(
            text="Показать другую дату", callback_data="action:another_date"
        )
    )
    markup.add(
            InlineKeyboardButton(
                text='Отмена', callback_data='action:cancel'
                )
            )

    return markup
