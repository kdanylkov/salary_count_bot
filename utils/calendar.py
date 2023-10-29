from loader import calendar, calendar_1_callback
import datetime


def get_calendar(now, calendar_callback=calendar_1_callback):
    calendar_keyboard = calendar.create_calendar(
        name=calendar_callback.prefix,
        year=now.year,
        month=now.month,
    )

    return calendar_keyboard


def get_first_and_last_dates(
        month: int, year: int
) -> tuple[datetime, datetime]:
    first_day = datetime.date(year, month, 1)

    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)
    last_day = next_month - datetime.timedelta(days=1)

    return first_day, last_day
