from django.db import models

from apps.model.portfolios import Portfolios
from apps.model.stocks import Stocks


class PortfoliosDetailQuerySet(models.QuerySet):

    def purchase(self, purchase_date: str, stock_count: int, portfolio_id: int, stock_code: int):
        self.create(
            purchase_date = purchase_date,
            stock_count = stock_count,
            portfolio_id = Portfolios.objects.get(id = portfolio_id),
            stocks_id = Stocks.objects.get(stock_code = stock_code),
        )


class PortfoliosDetail(models.Model):
    objects = PortfoliosDetailQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    purchase_date = models.DateField(auto_now_add = True, db_column = 'purchase_date')
    sell_date = models.DateField(default = None, null = True, db_column = 'sell_date')
    stock_count = models.IntegerField(blank = False, null = False, default = 0, db_column = 'stock_count')

    portfolio_id = models.ForeignKey(Portfolios, on_delete = models.DO_NOTHING, db_column = 'portfolio_id')
    stocks_id = models.ForeignKey(Stocks, on_delete = models.DO_NOTHING, db_column = 'stocks_id')

    class Meta:
        managed = False
        db_table = 'portfolios_detail'
