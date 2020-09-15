import os

import FinanceDataReader as fdr
import matplotlib.pyplot as plt

from apps.third_party.fdr.finance_data import FinanceData
from apps.third_party.util.utils import today_dateformat
from sample.settings import MEDIA_ROOT


class FinanceDataStocks(FinanceData):

    def __init__(self, symbol: str, start_date: str = '1991', end_date: str = None):
        """
        :param symbol: 주식코드(ex, 005930) / 환율(ex, USD/KRW) / Ticker(ex, QQQ)
        :param start_date: 시작날짜 (ex, 1991-01-01) (default : 1991-01-01)
        :param end_date: 종료날짜 (ex, 2020-01-01) (default : today)
        :type end_date: default None
        """
        super().__init__()
        self._symbol = symbol

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

    def get_data_frame(self):
        return fdr.DataReader(self._symbol, self._start_date, self._end_date)

    def save_image(self):
        image_path = _get_image_path(self._symbol, self._start_date, self._end_date)
        if os.path.exists(image_path):  # 파일이 있으니까 로직 작동 X
            return False

        df = self.get_data_frame()
        df['Close'].plot()
        plt.savefig(image_path)
        return True

    def get_save_image_path(self):
        return '{}/{}'.format(_replace_symbol(self._symbol), _get_filename(self._start_date, self._end_date))


##########################################################################################

def _replace_symbol(symbol: str):
    symbol = symbol.replace('/', '')
    return symbol


def _get_filename(start_date: str, end_date: str):
    filename = '{}_{}.png'.format(start_date, end_date)
    return filename


def _get_image_path(symbol: str, start_date: str, end_date: str):
    base_path = os.path.join(MEDIA_ROOT, _replace_symbol(symbol))
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    return os.path.join(base_path, _get_filename(start_date, end_date))
