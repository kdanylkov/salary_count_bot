from telebot.util import quick_markup


def one_more_visit():
    return quick_markup(
        {
            "Еще одно посещение": {"callback_data": "one_more_visit:yes"},
            "Обзор рабочего дня": {"callback_data": "one_more_visit:overview"},
            "Отмена": {"callback_data": "one_more_visit:cancel"},
        }
    )
