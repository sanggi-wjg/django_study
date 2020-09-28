from django.db import models

from apps.model.portfolios import Portfolios
from apps.model.stocks import Stocks


class Portfolios_detail(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')

    start_date = models.CharField(max_length = 10, null = False, db_column = 'start_date')
    end_date = models.CharField(max_length = 10, null = True, default = None, db_column = 'end_date')

    portfolio_id = models.ForeignKey(Portfolios, on_delete = models.DO_NOTHING, db_column = 'portfolio_id')
    stocks_id = models.ForeignKey(Stocks, on_delete = models.DO_NOTHING, db_column = 'stocks_id')

    class Meta:
        managed = False
        db_table = 'portfolios_detail'
