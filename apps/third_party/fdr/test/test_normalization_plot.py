import pandas as pd
import numpy as np
import pytest
import FinanceDataReader as fdr

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks


@pytest.mark.django_db
def test_stock():
    kospi_list = fdr.DataReader('KS11', '2010-01-01')
    samsung_list = StockPrice.objects.values('close_price', 'date').filter(
        stocks_id = Stocks.objects.get(stock_name = '삼성전자'),
        date__gte = '2010-01-01', date__lte = '2020-11-16'
    ).order_by('date')

    sk_list = StockPrice.objects.values('close_price', 'date').filter(
        stocks_id = Stocks.objects.get(stock_name = 'SK하이닉스'),
        date__gte = '2010-01-01', date__lte = '2020-11-16'
    ).order_by('date')

    dataframe = pd.DataFrame(index = [p['date'] for p in samsung_list])
    dataframe['KOSPI'] = kospi_list['Close']
    dataframe['Samsung'] = [p['close_price'] for p in samsung_list]
    dataframe['SK_Hynix'] = [p['close_price'] for p in sk_list]

    mean = dataframe.mean(axis = 0)
    std = dataframe.std(axis = 0)

    print()
    print(dataframe)
    print(mean)
    print(std)

    dataframe['Samsung_Normalization'] = (dataframe['Samsung'] - mean['Samsung']) / std['Samsung']
    dataframe['SK_Hynix_Normalization'] = (dataframe['SK_Hynix'] - mean['SK_Hynix']) / std['SK_Hynix']
    dataframe['KOSPI_Normalization'] = (dataframe['KOSPI'] - mean['KOSPI']) / std['KOSPI']
    print(dataframe)

    locator = mdates.MonthLocator()
    formatter = mdates.DateFormatter('%Y')
    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["figure.figsize"] = (30, 20)
    plt.rcParams["axes.grid"] = True
    plt.rcParams['font.size'] = 20

    plt.subplot(211)
    plt.plot(dataframe['Samsung'], label = 'Samsung')
    plt.plot(dataframe['SK_Hynix'], label = 'SK_Hynix')
    plt.legend(loc = 'upper right')

    plt.subplot(212)
    plt.plot(dataframe['Samsung_Normalization'], label = 'Samsung')
    plt.plot(dataframe['SK_Hynix_Normalization'], label = 'SK_Hynix')
    plt.plot(dataframe['KOSPI_Normalization'], label = 'KOSPI')
    plt.legend(loc = 'upper right')

    plt.show()
    plt.close()
