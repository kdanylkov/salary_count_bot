from datetime import datetime, timedelta


def range_of_dates(start_date: datetime, end_date: datetime):
    delta = end_date - start_date

    for i in range(delta.days + 1):
        yield start_date + timedelta(days=i)
