import os

import matplotlib.pyplot as plt
import FinanceDataReader as fdr
import pandas as pd
from typing import Tuple

from apps.third_party.util.colorful import print_yellow
from apps.third_party.util.utils import today_dateformat, validate_path
from sample.settings import MEDIA_ROOT


class FinanceDataImage:
    """
    https://github.com/FinanceData/FinanceDataReader
    """
    save_path: list = []

    def __init__(self, start_date: str, end_date: str = None):
        """
        :param start_date: 시작날짜 (ex, 1991-01-01) (default : 1991-01-01)
        :param end_date: 종료날짜 (ex, 2020-01-01) (default : today)
        :type end_date: default None
        """
        plt.rcParams["font.family"] = 'NanumGothic'
        plt.rcParams["figure.figsize"] = (14, 6)
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

        self._file_name = '{}_{}.png'.format(self._start_date, self._end_date)

    def finance_data_frame(self, symbol):
        """
        :param symbol: If is_str, 주식코드(ex, 005930) / 환율(ex, USD/KRW) / Ticker(ex, QQQ)
                       If is_list, [ [주식명, 주식코드] ... ]
        """
        if isinstance(symbol, str):
            df = fdr.DataReader(symbol, self._start_date, self._end_date)['Close']

        elif isinstance(symbol, list):
            df_list = [fdr.DataReader(stock_code, self._start_date, self._end_date)['Close'] for stock_name, stock_code in symbol]
            df = pd.concat(df_list, axis = 1)
            df.columns = [stock_name for stock_name, stock_code in symbol]

        else:
            raise TypeError('Data type of symbol is not allowed.')

        # print_yellow(df)
        return df

    def _get_save_image_path(self) -> str:
        return '{}/{}'.format('/'.join(self.save_path), self._file_name)

    def _validate_save_path(self) -> str:
        filepath = os.path.join(MEDIA_ROOT)
        for path in self.save_path:
            filepath = os.path.join(filepath, path)
            validate_path(filepath)

        return filepath

    def _get_full_path(self, media_path: str) -> str:
        if not self.save_path:
            raise NotImplementedError('save_path is not declared')

        self.save_path.append(_replace(media_path))
        save_path = self._validate_save_path()
        return os.path.join(save_path, self._file_name)

    def save_image(self, symbol, media_path: str) -> Tuple[bool, str]:
        """
        :param symbol: If is_str, 주식코드(ex, 005930) / 환율(ex, USD/KRW) / Ticker(ex, QQQ)
                       If is_list, [ [주식명, 주식코드] ... ]
        :param media_path: path in media folder
        :return: If create new plot image file, then return True.
                 Otherwise return False.
        """
        full_path = self._get_full_path(media_path)
        if os.path.exists(full_path):  # 파일이 있으니까 밑에꺼는 작동할 필요가 읍다
            return False, self._get_save_image_path()

        data_frame = self.finance_data_frame(symbol)
        data_frame.plot()
        plt.savefig(full_path)
        plt.close('all')

        return True, self._get_save_image_path()


def _replace(text: str) -> str:
    text = text.replace('/', '')
    return text
