from django.db import models
from django.shortcuts import get_object_or_404

from apps.model.stocks import Stocks


class PivotQuerySet(models.QuerySet):

    def register(self, stock_code, pivot_form):
        pivot = pivot_form.save(commit = False)
        pivot.stocks_id = get_object_or_404(Stocks, code = stock_code)
        pivot.base_line = (pivot.prev_closing_price + pivot.prev_low_price + pivot.prev_high_price) / 3
        pivot.resist_line_1 = (pivot.base_line * 2) - pivot.prev_low_price
        pivot.resist_line_2 = pivot.base_line + (pivot.prev_high_price - pivot.prev_low_price)
        pivot.resist_line_3 = pivot.prev_high_price + (pivot.base_line - pivot.prev_low_price) * 2
        pivot.support_line_1 = (pivot.base_line * 2) - pivot.prev_high_price
        pivot.support_line_2 = pivot.base_line - (pivot.prev_high_price - pivot.prev_low_price)
        pivot.support_line_3 = pivot.prev_low_price - (pivot.prev_high_price - pivot.base_line) * 2
        pivot.recommend_high_price = (pivot.resist_line_1 + pivot.base_line) / 2
        pivot.recommend_low_price = (pivot.base_line + pivot.support_line_1) / 2
        pivot.save()


class Pivot(models.Model):
    objects = PivotQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')
    stocks_id = models.ForeignKey(Stocks, on_delete = models.DO_NOTHING, db_column = 'stocks_id')

    prev_closing_price = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'prev_closing_price')
    prev_high_price = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'prev_high_price')
    prev_low_price = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'prev_low_price')

    resist_line_3 = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'resist_line_3')
    resist_line_2 = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'resist_line_2')
    resist_line_1 = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'resist_line_1')

    base_line = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'base_line')

    support_line_1 = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'support_line_1')
    support_line_2 = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'support_line_2')
    support_line_3 = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'support_line_3')

    recommend_high_price = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'recommend_high_price')
    recommend_low_price = models.PositiveIntegerField(blank = False, null = False, default = 0, db_column = 'recommend_low_price')

    date = models.DateField(auto_now = True, db_column = 'date')
