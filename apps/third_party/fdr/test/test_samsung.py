import pandas as pd
import numpy as np
import pytest
import FinanceDataReader as fdr

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks

START_DATE = '2000-01-01'


@pytest.mark.django_db
def test_stock():
    samsung_list = StockPrice.objects.values('close_price', 'date').filter(
        stocks_id = Stocks.objects.get(stock_name = '삼성전자'),
        date__gte = START_DATE
    ).order_by('date')

    samsung_woo_list = fdr.DataReader('005935', START_DATE)

    dataframe = pd.DataFrame(index = [p['date'] for p in samsung_list])
    dataframe['Samsung'] = [p['close_price'] for p in samsung_list]
    dataframe['Samsung_Woo'] = samsung_woo_list['Close']

    dataframe['Diff'] = round((dataframe['Samsung_Woo'] / dataframe['Samsung']) * 100)
    print()
    print(dataframe)

    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["figure.figsize"] = (30, 20)
    plt.rcParams["axes.grid"] = True
    plt.rcParams['font.size'] = 20

    plt.subplot(211)
    plt.plot(dataframe['Samsung'], label = '삼성전자')
    plt.plot(dataframe['Samsung_Woo'], label = '삼성전자 우선주')
    plt.legend(loc = 'upper right')

    plt.subplot(212)
    plt.plot(dataframe['Diff'], label = '비교')
    plt.legend(loc = 'upper right')

    plt.show()
    plt.close()
