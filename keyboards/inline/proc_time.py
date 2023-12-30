from telebot.util import quick_markup
from telebot.types import InlineKeyboardButton


def get_times_makrup():
    markup = quick_markup(
        {
            time: {'callback_data': f'time:{time}'}
            for time
            in get_proc_times_list()
        },
        row_width=4
    )
    btn_custom_time = InlineKeyboardButton(
        'Своё время', callback_data='time:custom')
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='time:cancel')

    markup.add(btn_custom_time, btn_cancel)

    return markup


def get_proc_times_list():
    times_unformatted = [
        str(num) for num
        in range(1000, 2001, 50)
    ]

    times_unformatted_with_half_hour = [
        ''.join([time[:2], '3', time[3:]])
        if time[2] == '5' else time
        for time in times_unformatted
    ]

    times_formatted = [
        ''.join([time[:2], ':', time[2:]])
        for time
        in times_unformatted_with_half_hour
    ]

    return times_formatted
