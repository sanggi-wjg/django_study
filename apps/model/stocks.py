from django.db import models

from apps.model.industries import Industries
from apps.model.sectors import Sectors


class StocksQuerySet(models.QuerySet):

    def get_detail_join_one(self, stock_code):
        data = self.select_related('sectors_id').values(
            'id', 'stock_name', 'stock_code', 'sectors_id__sector_name'
        ).get(stock_code = stock_code)

        return data


class Stocks(models.Model):
    objects = StocksQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    stock_market = models.CharField(max_length = 10, null = False, db_column = 'stock_market')
    stock_code = models.CharField(max_length = 10, unique = True, null = False, db_column = 'stock_code')
    stock_name = models.CharField(max_length = 50, unique = True, null = False, db_column = 'stock_name')

    sectors_id = models.ForeignKey(Sectors, on_delete = models.DO_NOTHING, db_column = 'sectors_id')
    industries_id = models.ForeignKey(Industries, on_delete = models.DO_NOTHING, db_column = 'industries_id')

    def __str__(self):
        return '[{}] {}({})'.format(self.stock_market, self.stock_name, self.stock_code)

    class Meta:
        managed = True
        db_table = 'stocks'
