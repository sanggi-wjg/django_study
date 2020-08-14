from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404

"""
python manage.py makemigrations stock

python manage.py sqlmigrate stock 0001

python manage.py migrate stock

* Drop table 후 table 생성이 안되면... 하고 다시 migrate
python manage.py migrate --fake stock zero
"""


class Section_Multiple(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')
    multiple = models.FloatField(blank = False, null = False, default = 1.0, db_column = 'multiple')

    def __str__(self):
        return '[{} : {}]'.format(self.id, self.multiple)


class Section_Name(models.Model):
    id = models.AutoField(primary_key = True, db_column = '')
    name = models.CharField(blank = False, null = False, default = '', max_length = 20, unique = True, db_column = 'name')

    def __str__(self):
        return self.name


class ItemsQuerySet(models.QuerySet):

    def get_detail_join_one(self, stock_code):
        data = self.select_related('stock_section_name_id', 'stock_section_multiple_id').values(
            'id', 'name', 'code', 'stock_section_multiple_id__multiple', 'stock_section_name_id__name'
        ).get(code = stock_code)

        return data


class Items(models.Model):
    objects = ItemsQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')
    stock_section_name_id = models.ForeignKey(Section_Name, on_delete = models.DO_NOTHING, db_column = 'stock_section_name_id')
    stock_section_multiple_id = models.ForeignKey(Section_Multiple, on_delete = models.DO_NOTHING, db_column = 'stock_section_multiple_id')

    code = models.CharField(max_length = 10, unique = True, db_column = 'code')
    name = models.CharField(max_length = 100, unique = True, db_column = 'name')

    def __str__(self):
        return '[{}] {}({})'.format(self.id, self.code, self.name)


class PivotQuerySet(models.QuerySet):

    def register(self, stock_code, pivot_form):
        pivot = pivot_form.save(commit = False)
        pivot.stock_items_id = get_object_or_404(Items, code = stock_code)
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
    stock_items_id = models.ForeignKey(Items, on_delete = models.DO_NOTHING, db_column = 'stock_items_id')

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

    def __str__(self):
        return '({}) stock_items_id : {}'.format(self.date, self.stock_items_id)
