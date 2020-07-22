from datetime import datetime


def today_dateformat(time_format = '%Y-%m-%d %H:%M:%S'):
    return datetime.today().strftime(time_format)
