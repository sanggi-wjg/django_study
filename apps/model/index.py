from django.db import models


class IndexQuerySet(models.QuerySet):

    def get_index_df(self, index_name: str, start_date: str, end_date: str):
        result = self.values('number', 'date').filter(
            index_name = index_name, date__gte = start_date, date__lte = end_date
        )

        return result


class Index(models.Model):
    objects = IndexQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    index_name = models.CharField(max_length = 45, null = False, db_column = 'index_name')
    number = models.IntegerField(null = False, db_column = 'number')
    date = models.DateField(null = False, db_column = 'date')

    class Meta:
        managed = False
        db_table = 'index'

    def __str__(self):
        return '[{} - {}] {}'.format(self.index_name, self.date, self.number)
