import os

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from typing import Tuple

from apps.third_party.fdr.finance_data import FinanceData, _replace_symbol, _get_filename
from apps.third_party.util.utils import validate_media_path
from sample.settings import MEDIA_ROOT


class FinanceDataBasic(FinanceData):
    _symbol = None

    def save_image(self, symbol: str) -> Tuple[bool, str]:
        """
        :param symbol: 주식코드(ex, 005930) / 환율(ex, USD/KRW) / Ticker(ex, QQQ)
        :return: If create new plot image file, then return True. Otherwise return False.
        """
        self._symbol = symbol

        image_path = _get_image_path(self._symbol, self._start_date, self._end_date)
        if os.path.exists(image_path):  # 파일이 있으니까 로직 작동 X
            return False, self._get_save_image_path()

        # 생성
        df = fdr.DataReader(self._symbol, self._start_date, self._end_date)
        df['Close'].plot()
        plt.savefig(image_path)

        return True, self._get_save_image_path()

    def _get_save_image_path(self) -> str:
        return 'finance/{}/{}'.format(_replace_symbol(self._symbol), _get_filename(self._start_date, self._end_date))


##########################################################################################


def _get_image_path(symbol: str, start_date: str, end_date: str) -> str:
    filepath = os.path.join(MEDIA_ROOT, 'finance')
    validate_media_path(filepath)

    filepath = os.path.join(filepath, _replace_symbol(symbol))
    validate_media_path(filepath)

    return os.path.join(filepath, _get_filename(start_date, end_date))
