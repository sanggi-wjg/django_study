from datetime import datetime, timedelta


def today_dateformat(time_format = '%Y-%m-%d %H:%M:%S'):
    return datetime.today().strftime(time_format)


def get_date(date: str, time_format) -> str:
    if not date:
        date = today_dateformat(time_format)

    date = datetime.strptime(date, time_format) - timedelta(days = 1)
    date = date.strftime(time_format)

    return date


def get_date_list(date_range: int, time_format: str = '%Y-%m-%d') -> list:
    date_list = []

    for n in range(1, date_range):
        day = datetime.strptime(get_date(today_dateformat(time_format), time_format), time_format) - timedelta(days = n)
        date_list.append(day.strftime(time_format))

    return date_list
