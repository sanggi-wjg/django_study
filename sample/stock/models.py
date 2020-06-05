from django.db import models

from .querysets import ItemsQuerySet

"""
python manage.py makemigrations stock

python manage.py sqlmigrate stock 0002

python manage.py migrate
"""


class Items(models.Model):
    id = models.AutoField(primary_key = True)
    code = models.CharField(max_length = 10)
    name = models.CharField(max_length = 100)

    objects = ItemsQuerySet.as_manager()

    def __str__(self):
        return '[{}] {}({})'.format(self.id, self.code, self.name)


class Pivot(models.Model):
    id = models.AutoField(primary_key = True)
    stock_items_id = models.ForeignKey(Items, on_delete = models.DO_NOTHING)

    prev_closing_price = models.PositiveIntegerField(blank = False, null = False, default = 0)
    prev_high_price = models.PositiveIntegerField(blank = False, null = False, default = 0)
    prev_low_price = models.PositiveIntegerField(blank = False, null = False, default = 0)

    resist_line_3 = models.PositiveIntegerField(blank = True, null = True, default = None)
    resist_line_2 = models.PositiveIntegerField(blank = True, null = True, default = None)
    resist_line_1 = models.PositiveIntegerField(blank = True, null = True, default = None)

    base_line = models.PositiveIntegerField(blank = True, null = True, default = None)

    support_line_1 = models.PositiveIntegerField(blank = True, null = True, default = None)
    support_line_2 = models.PositiveIntegerField(blank = True, null = True, default = None)
    support_line_3 = models.PositiveIntegerField(blank = True, null = True, default = None)

    date = models.DateField(blank = True, null = True, default = None)
