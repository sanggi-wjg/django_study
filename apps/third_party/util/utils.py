import os
from datetime import datetime, timedelta

import json
import psutil
import xmltodict


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


def gmt_to_est_datetime(gmt_date: str, gmt_format: str = '%a, %d %b %Y %H:%M:%S %z', est_format: str = '%Y-%m-%d %H:%M:%S'):
    gmt = datetime.strptime(gmt_date, gmt_format)
    gmt = gmt.strftime(est_format)
    est = datetime.strptime(gmt, est_format)
    return est


def current_year_subtract(delta: int, time_format: str = '%Y'):
    current_year = datetime.today().strftime(time_format)
    date = datetime.strptime(current_year, time_format) - timedelta(days = (int(delta) * 365))
    return date.strftime(time_format)


def current_month_subtract(delta: int, time_format: str = '%Y-%m'):
    current_year = datetime.today().strftime(time_format)
    date = datetime.strptime(current_year, time_format) - timedelta(days = (int(delta) * 30))
    return date.strftime(time_format)


def current_day_subtract(delta: int, time_format: str = '%Y-%m-%d'):
    current_year = datetime.today().strftime(time_format)
    date = datetime.strptime(current_year, time_format) - timedelta(days = delta)
    return date.strftime(time_format)


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


def get_cpu_count() -> int:
    return psutil.cpu_count()


def xml_to_dict(xml: str) -> dict:
    xml = xmltodict.parse(xml)
    return json.loads(json.dumps(xml))
