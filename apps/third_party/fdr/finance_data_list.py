import os

import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

from pandas import DataFrame
from typing import Tuple

from apps.third_party.fdr.finance_data import FinanceData, _get_filename
from apps.third_party.util.utils import validate_media_path
from sample.settings import MEDIA_ROOT


class FinanceDataList(FinanceData):
    _symbol_list = None
    _sector_id = None

    def get_fd_data(self) -> DataFrame:
        """
        :return: concat dataframe
        """
        df_list = [fdr.DataReader(stock_code, self._start_date, self._end_date)['Close'] for stock_name, stock_code in self._symbol_list]
        df = pd.concat(df_list, axis = 1)
        df.columns = [stock_name for stock_name, stock_code in self._symbol_list]

        return df

    def save_compared_stock_price_image(self, symbol_list: list, sector_id: str) -> Tuple[bool, str]:
        """
        :param sector_id: 섹터 id
        :param symbol_list: [ [주식명, 주식코드] ... ]
        :return: If create new plot image file, then return True. Otherwise return False.
        """
        self._symbol_list = symbol_list
        self._sector_id = sector_id

        image_path = _get_image_path(sector_id, self._start_date, self._end_date)
        if os.path.exists(image_path):  # 파일이 있으니까 로직 작동 X
            return False, self._get_compared_stock_price_image_path()

        # 생성
        df = self.get_fd_data()
        df.plot()
        plt.rcParams["font.family"] = 'nanummyeongjo'
        plt.savefig(image_path)

        return True, self._get_compared_stock_price_image_path()

    def _get_compared_stock_price_image_path(self) -> str:
        return 'finance/sector/{}/{}'.format(self._sector_id, _get_filename(self._start_date, self._end_date))


##########################################################################################


def _get_image_path(sector_id: str, start_date: str, end_date: str) -> str:
    filepath = os.path.join(MEDIA_ROOT, 'finance')
    validate_media_path(filepath)

    filepath = os.path.join(filepath, 'sector')
    validate_media_path(filepath)

    filepath = os.path.join(filepath, sector_id)
    validate_media_path(filepath)

    return os.path.join(filepath, _get_filename(start_date, end_date))
