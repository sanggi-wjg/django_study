from django.db import models

from apps.model.stocks import Stocks


class StockSubsQuerySet(models.QuerySet):

    def subscribe(self, stock_name: str):
        """
        구독 하기
        """
        try:
            stock = Stocks.objects.get(stock_name = stock_name)
            self.get(stocks_id = stock.id)

        except Stocks.DoesNotExist:
            # 주식이 없으면 에러
            raise Stocks.DoesNotExist
        except StockSubs.DoesNotExist:
            # 구독중이지 않으면 생성
            self.create(stocks_id = stock)

    def unsubscribe(self, stock_name):
        """
        구독 끊기
        """
        try:
            stock = Stocks.objects.get(stock_name = stock_name)
            self.filter(stocks_id = stock).delete()

        except Stocks.DoesNotExist:
            # 주식이 없으면 에러
            raise Stocks.DoesNotExist


class StockSubs(models.Model):
    objects = StockSubsQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')
    stocks_id = models.ForeignKey(Stocks, on_delete = models.DO_NOTHING, db_column = 'stocks_id')

    class Meta:
        managed = False
        db_table = 'stock_subs'
