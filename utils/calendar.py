from loader import calendar, calendar_1_callback


def get_calendar(now, calendar_callback=calendar_1_callback):
    calendar_keyboard = calendar.create_calendar(
        name=calendar_callback.prefix,
        year=now.year,
        month=now.month,
    )

    return calendar_keyboard
