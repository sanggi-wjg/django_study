from django.db import models

from apps.model.stocks import Stocks
from apps.third_party.util.utils import today_dateformat


class StockPriceQuerySet(models.QuerySet):

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
