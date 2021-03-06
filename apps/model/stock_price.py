from django.db import models

from apps.model.stocks import Stocks
from apps.third_party.util.utils import today_dateformat


class StockPriceQuerySet(models.QuerySet):

    def current_rsi(self, stock_name: str) -> float:
        """
        https://www.macroption.com/rsi-calculation/
        """
        N = 14
        price_list = StockPrice.objects.values('close_price', 'date').filter(
            stocks_id = Stocks.objects.get(stock_name = stock_name).id
        ).order_by('-date')[0:N + 1]
        price_list = sorted(price_list, key = lambda key: key['date'])

        AU, AD = 0.0, 0.0

        for i in range(1, len(price_list)):
            change = price_list[i]['close_price'] - price_list[i - 1]['close_price']

            if change > 0:
                AU += change
            else:
                AD += abs(change)

        AU, AD = AU / N, AD / N
        RS = AU / AD
        RSI = round((RS / (1 + RS)) * 100, 2)

        return RSI

    def get_stock_price_for_df(self, stocks_id: int, start_date: str, end_date: str):
        return self.values('close_price', 'date').filter(
            stocks_id = stocks_id,
            date__gte = start_date, date__lte = end_date
        )

    def get_last_date(self, stocks_id: int):
        result = self.values('date').filter(stocks_id = stocks_id).last()
        if result:
            return result['date']

        # return '2020-10-01'
        return '1990-01-01'

    def register(self, stocks_id: int, date: str, open_price: int, high_price: int, low_price: int, close_price: int):
        try:
            self.get(date = date, stocks_id = stocks_id)

            if date == today_dateformat(time_format = '%Y-%m-%d'):
                self.filter(date = date, stocks_id = stocks_id).update(
                    open_price = open_price,
                    high_price = high_price,
                    low_price = low_price,
                    close_price = close_price,
                )

        except StockPrice.DoesNotExist:
            self.create(
                date = date,
                open_price = open_price,
                high_price = high_price,
                low_price = low_price,
                close_price = close_price,
                stocks_id = Stocks.objects.get(id = stocks_id)
            )


class StockPrice(models.Model):
    objects = StockPriceQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    open_price = models.IntegerField(blank = False, null = False, db_column = 'open_price')
    high_price = models.IntegerField(blank = False, null = False, db_column = 'high_price')
    low_price = models.IntegerField(blank = False, null = False, db_column = 'low_price')
    close_price = models.IntegerField(blank = False, null = False, db_column = 'close_price')
    date = models.DateField(blank = False, null = False, db_column = 'date')

    stocks_id = models.ForeignKey(Stocks, on_delete = models.DO_NOTHING, db_column = 'stocks_id')

    class Meta:
        managed = False
        db_table = 'stock_price'

    def __str__(self):
        return '{} {} {}'.format(self.date, self.stocks_id.stock_name, self.close_price)
