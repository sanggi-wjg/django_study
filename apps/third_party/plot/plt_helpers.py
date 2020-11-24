import os
import matplotlib.dates as mdates

from apps.third_party.util.utils import validate_path
from sample.settings import MEDIA_ROOT


def plt_year_format():
    return mdates.YearLocator(), mdates.DateFormatter('%Y')


def plt_year_month_format():
    return mdates.MonthLocator(), mdates.DateFormatter('%Y-%M')


def plt_path(filedir: str, filename: str):
    path = os.path.join(MEDIA_ROOT, 'plt')
    validate_path(path)

    path = os.path.join(path, filedir)
    validate_path(path)

    return os.path.join(path, filename)


def plt_colors(no):
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
    return colors[no % len(colors)]
