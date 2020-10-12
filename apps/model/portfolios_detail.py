from django.db import models
from django.db.models import Count, F, Sum

from apps.model.portfolios import Portfolios
from apps.model.stocks import Stocks


class PortfoliosDetailQuerySet(models.QuerySet):

    def get_groups(self, portfolio_id: int):
        return self.values(
            'sell_date', 'stocks_id__stock_name', 'stocks_id', 'stocks_id__stock_code',
        ).annotate(
            total_stock_count = Sum('stock_count'),
            purchase_date = F('purchase_date')
        ).filter(
            portfolio_id = portfolio_id
        )

    def purchase(self, purchase_date: str, stock_count: int, portfolio_id: int, stock_code: int):
        try:
            # 해당 날짜로 해당 종목이 있으면 Update
            stocks_id = Stocks.objects.get(stock_code = stock_code).id
            portfolio = self.get(portfolio_id = portfolio_id, stocks_id = stocks_id)

            self.filter(
                portfolio_id = portfolio_id,
                stocks_id = stocks_id
            ).update(
                stock_count = stock_count + portfolio.stock_count
            )
        except PortfoliosDetail.DoesNotExist:
            # 없으면 Insert
            self.create(
                purchase_date = purchase_date,
                stock_count = stock_count,
                portfolio_id = Portfolios.objects.get(id = portfolio_id),
                stocks_id = Stocks.objects.get(stock_code = stock_code),
            )


class PortfoliosDetail(models.Model):
    objects = PortfoliosDetailQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    purchase_date = models.DateField(blank = False, null = False, db_column = 'purchase_date')
    sell_date = models.DateField(default = None, null = True, db_column = 'sell_date')
    stock_count = models.IntegerField(blank = False, null = False, default = 0, db_column = 'stock_count')

    portfolio_id = models.ForeignKey(Portfolios, on_delete = models.DO_NOTHING, db_column = 'portfolio_id')
    stocks_id = models.ForeignKey(Stocks, on_delete = models.DO_NOTHING, db_column = 'stocks_id')

    class Meta:
        managed = False
        db_table = 'portfolios_detail'
