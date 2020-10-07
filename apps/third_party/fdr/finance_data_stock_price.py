import FinanceDataReader as fdr

from apps.model.stock_price import StockPrice
from apps.third_party.util.colorful import print_yellow


class FinanceDataStockPrice:

    def register(self, stocks_id: str, stock_code: str, **kwargs):
        last_date = StockPrice.objects.get_last_date(stocks_id)

        df = fdr.DataReader(stock_code, last_date)
        for date, row in df.iterrows():
            print_yellow('{} {} 등록'.format(kwargs.get('stock_name'), date.strftime('%Y-%m-%d')))
            StockPrice.objects.register(stocks_id, date.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'])
