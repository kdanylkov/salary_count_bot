from telebot.util import quick_markup


def if_subscr_laser():
    return quick_markup(
        {
            "Разовое посещение": {"callback_data": "laser_sub_no"},
            "Абонимент(ы)": {"callback_data": "laser_sub_yes"},
            "Ввести вручную": {"callback_data": "laser_sub_manual"},
        },
        row_width=2,
    )


def if_another_subscr():
    return quick_markup(
        {
            "Да": {"callback_data": "plus_subscr_yes"},
            "Нет": {"callback_data": "plus_subscr_no"},
        }
    )
