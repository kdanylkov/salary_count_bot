from telebot.util import quick_markup


def if_full_report():
    return quick_markup(
        {
            "Скачать детальный отчет": {"callback_data": "full_report:yes"},
            "Отмена": {"callback_data": "full_report:cancel"},
        }
    )
