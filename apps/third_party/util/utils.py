import os
from datetime import datetime, timedelta

from sample.settings import MEDIA_ROOT


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


def current_year_subtract(delta: int):
    current_year = datetime.today().strftime('%Y')
    date = datetime.strptime(current_year, '%Y') - timedelta(days = (int(delta) * 365))
    return date.strftime('%Y')


def current_month_subtract(delta: int):
    current_year = datetime.today().strftime('%Y-%m')
    date = datetime.strptime(current_year, '%Y-%m') - timedelta(days = (int(delta) * 30))
    return date.strftime('%Y-%m')


def validate_path(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
    return True


def escape_number(text):
    text = text.replace(',', '')
    text = text.replace('+', '')
    text = text.replace('--', '-')
    return text


def escape_char(text):
    text = text.replace('%', '')
    return text
