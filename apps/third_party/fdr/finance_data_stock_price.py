import FinanceDataReader as fdr
from django.db.models import Count, F

from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stock_price import StockPrice
from apps.third_party.util.colorful import print_yellow


class FinanceDataStockPrice:

    def _get_stock_list(self):
        return PortfoliosDetail.objects.values(
            'stocks_id__stock_code', 'stocks_id__stock_name'
        ).annotate(
            stock_count = Count('stocks_id'),
            stocks_id = F('stocks_id'),
        )

    def register(self):
        stock_list = self._get_stock_list()

        for stock in stock_list:
            last_date = StockPrice.objects.get_last_date(stock['stocks_id'])

            df = fdr.DataReader(stock['stocks_id__stock_code'], last_date)
            for date, row in df.iterrows():
                print_yellow('{} {} 등록'.format(stock['stocks_id__stock_name'], date.strftime('%Y-%m-%d')))
                StockPrice.objects.register(stock['stocks_id'], date.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'])
