from telebot.util import quick_markup


def if_delete_visit():
    return quick_markup(
        {
            "Удалить посещение": {"callback_data": "chan_del_delete"},
            "Изменить процедуру": {"callback_data": "chan_del_change"},
            "Отмена": {"callback_data": "chan_del_cancel"},
        },
        row_width=2,
    )
