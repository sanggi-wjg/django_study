from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models


class PortfoliosQuerySet(models.QuerySet):

    def is_exist_portfolio_name(self, portfolio_name: str) -> bool:
        try:
            self.get(portfolio_name = portfolio_name)
        except Portfolios.DoesNotExist:
            return False

        return True

    def register(self, portfolio_name: str, portfolio_deposit: int, user_id: int):
        result = self.create(
            portfolio_name = portfolio_name,
            portfolio_deposit = int(portfolio_deposit),
            user_id = User.objects.get(id = user_id)
        )
        return result

    def update_date(self):
        pass


class Portfolios(models.Model):
    objects = PortfoliosQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    portfolio_name = models.CharField(max_length = 50, null = False, db_column = 'portfolio_name')
    portfolio_deposit = models.IntegerField(blank = False, null = False, db_column = 'portfolio_deposit')
    portfolio_purchase_price = models.IntegerField(blank = False, null = False, default = 0, db_column = 'portfolio_purchase_price')
    portfolio_sales = models.IntegerField(blank = False, null = False, default = 0, db_column = 'portfolio_sales')

    register_date = models.DateField(auto_now_add = True, db_column = 'register_date')
    update_date = models.DateField(auto_now = True, db_column = 'update_date')

    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.DO_NOTHING, db_column = 'user_id')

    class Meta:
        managed = False
        db_table = 'portfolios'

    def __str__(self):
        return '{} : {} / {} / {}'.format(self.user_id, self.portfolio_name, self.portfolio_deposit, self.portfolio_sales)
