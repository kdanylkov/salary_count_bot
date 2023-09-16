from telebot.util import quick_markup


def if_delete_visit():
    return quick_markup(
        {
            "Удалить посещение": {"callback_data": "if_delete_visit_yes"},
            "Отмена": {"callback_data": "if_delete_visit_cancel"},
        },
        row_width=2,
    )
