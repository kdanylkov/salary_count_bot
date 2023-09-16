from telebot.util import quick_markup


def visits_markup():
    return quick_markup(
        {num: {"callback_data": f"visits_count_{num}"} for num in range(1, 7)},
        row_width=3,
    )
