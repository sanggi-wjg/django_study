import FinanceDataReader as fdr

import pandas as pd
import pytest
from pandas import DataFrame

from apps.model.index import Index
from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks
from apps.third_party.plot.plt_utils import show_plot, show_plot_twinx, show_plot_twinx_list


@pytest.mark.django_db
def test_test():
    START_DATE, FINISH_DATE = '{}-01-01'.format(2000), '{}-12-31'.format(2020)

    # gold_index = Index.objects.values('number', 'date').filter(index_name = 'GOLD', date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
    # gold_df = convert_dataframe(gold_index)
    #
    # kopsi_index = Index.objects.values('number', 'date').filter(index_name = 'KOSPI', date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
    # kospi_df = convert_dataframe(kopsi_index)
    #
    # show_plot_twinx(gold_df, 'GOLD', kospi_df, 'KOSPI')

    df_usdkrw = fdr.DataReader('USD/KRW', START_DATE, FINISH_DATE)
    df_usdkrw['Close'] = df_usdkrw['Close']

    sinhan_price = StockPrice.objects.values('close_price', 'date').filter(stocks_id = Stocks.objects.get(stock_name = '신한지주').id, date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
    df_sinhan_price = convert_dataframe(sinhan_price, 'close_price')

    hana_price = StockPrice.objects.values('close_price', 'date').filter(stocks_id = Stocks.objects.get(stock_name = '하나금융지주').id, date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
    df_hana_price = convert_dataframe(hana_price, 'close_price')

    daesin_price = StockPrice.objects.values('close_price', 'date').filter(stocks_id = Stocks.objects.get(stock_name = '대신증권').id, date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
    df_daesin_price = convert_dataframe(daesin_price, 'close_price')

    ktng_price = StockPrice.objects.values('close_price', 'date').filter(stocks_id = Stocks.objects.get(stock_name = 'KT&G').id, date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
    df_ktng_price = convert_dataframe(ktng_price, 'close_price')

    df_usdkrw['SN'] = standard_normalization(df_usdkrw, 'Close')
    df_sinhan_price['SN'] = standard_normalization(df_sinhan_price, 'Price')
    df_hana_price['SN'] = standard_normalization(df_hana_price, 'Price')
    df_daesin_price['SN'] = standard_normalization(df_daesin_price, 'Price')
    df_ktng_price['SN'] = standard_normalization(df_ktng_price, 'Price')

    # show_plot_twinx_list(
    #     [df_sinhan_price, df_ktng_price], ['신한지주', 'KT&G'], 'Price',
    #     [df_usdkrw], ['환율'], '환율'
    # )

    show_plot_twinx_list(
        [df_sinhan_price['SN'], df_ktng_price['SN'], df_hana_price['SN'], df_daesin_price['SN']], ['신한지주', 'KT&G', '하나지주', '대신증권'], 'Price',
        [df_usdkrw['SN']], ['환율'], '환율'
    )


def convert_dataframe(data, price_key):
    df = pd.DataFrame([x[price_key] for x in data], index = [x['date'] for x in data], columns = ['Price'])
    return df


def standard_normalization(dataframe: DataFrame, column: str):
    mean = dataframe.mean(axis = 0)
    std = dataframe.std(axis = 0)

    return (dataframe[column] - mean[column]) / std[column]
