import os
import matplotlib.dates as mdates

from apps.third_party.util.utils import validate_path
from sample.settings import MEDIA_ROOT


def financial_crisis_list():
    return [
        ('1983-09-24', '1983-10-17', '검은 토요일'),
        ('1987-07-19', '1988-01-31', '검은 월요일'),
        ('1997-01-01', '1997-12-31', '동아시아 외환위기'),
        ('2000-01-01', '2001-03-30', 'IT 버블'),
        ('2001-09-11', '2001-12-31', '미국 911 테러'),
        ('2007-12-01', '2009-03-30', '글로벌 금융위기(서브프라임 모기지)'),
        ('2010-03-01', '2011-11-01', '유럽 금융위기'),
        ('2015-08-11', '2016-03-01', '위완화 평가절하 발표'),
        ('2020-03-01', '2020-04-01', '코로나'),
    ]


def plt_year_format():
    return mdates.YearLocator(), mdates.DateFormatter('%Y')


def plt_year_month_format():
    return mdates.MonthLocator(), mdates.DateFormatter('%Y-%M')


def plt_path(filedir: str, filename: str):
    path = os.path.join(MEDIA_ROOT, 'plt')
    validate_path(path)

    path = os.path.join(path, filedir)
    validate_path(path)

    return os.path.join(path, (filename + '.png'))


def plt_colors(no):
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
    return colors[no % len(colors)]
