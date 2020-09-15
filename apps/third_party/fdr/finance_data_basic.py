import os

import FinanceDataReader as fdr
import matplotlib.pyplot as plt

from apps.third_party.fdr.finance_data import FinanceData
from sample.settings import MEDIA_ROOT


class FinanceDataBasic(FinanceData):
    _symbol = None

    def save_image(self, symbol: str) -> bool:
        """
        :param symbol: 주식코드(ex, 005930) / 환율(ex, USD/KRW) / Ticker(ex, QQQ)
        :return: If create new plot image file, then return True. Otherwise return False.
        """
        self._symbol = symbol
        image_path = _get_image_path(self._symbol, self._start_date, self._end_date)
        if os.path.exists(image_path):  # 파일이 있으니까 로직 작동 X
            return False

        df = fdr.DataReader(self._symbol, self._start_date, self._end_date)
        df['Close'].plot()
        plt.savefig(image_path)
        return True

    def get_save_image_path(self) -> str:
        return '{}/{}'.format(_replace_symbol(self._symbol), _get_filename(self._start_date, self._end_date))


##########################################################################################

def _replace_symbol(symbol: str) -> str:
    symbol = symbol.replace('/', '')
    return symbol


def _get_filename(start_date: str, end_date: str) -> str:
    filename = '{}_{}.png'.format(start_date, end_date)
    return filename


def _get_image_path(symbol: str, start_date: str, end_date: str) -> str:
    base_path = os.path.join(MEDIA_ROOT, _replace_symbol(symbol))
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    return os.path.join(base_path, _get_filename(start_date, end_date))
