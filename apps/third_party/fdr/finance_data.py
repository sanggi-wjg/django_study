import matplotlib.pyplot as plt

from apps.third_party.util.utils import today_dateformat


class FinanceData:
    """
    https://github.com/FinanceData/FinanceDataReader
    """

    def __init__(self, start_date: str = '1991', end_date: str = None):
        """
                :param symbol: 주식코드(ex, 005930) / 환율(ex, USD/KRW) / Ticker(ex, QQQ)
                :param start_date: 시작날짜 (ex, 1991-01-01) (default : 1991-01-01)
                :param end_date: 종료날짜 (ex, 2020-01-01) (default : today)
                :type end_date: default None
                """
        plt.rcParams["font.family"] = 'nanummyeongjo'
        plt.rcParams["figure.figsize"] = (14, 4)
        plt.rcParams['lines.linewidth'] = 2
        plt.rcParams["axes.grid"] = True

        if len(start_date) == 4:
            self._start_date = start_date + '-01-01'
        elif len(start_date) == 7:
            self._start_date = start_date + '-01'
        else:
            self._start_date = start_date

        if end_date is None:
            self._end_date = today_dateformat(time_format = '%Y-%m-%d')
        else:
            self._end_date = end_date
