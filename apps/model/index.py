from django.db import models


class Index(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')

    index_name = models.CharField(max_length = 45, null = False, db_column = 'index_name')
    number = models.IntegerField(null = False, db_column = 'number')
    date = models.DateField(null = False, db_column = 'date')

    class Meta:
        managed = False
        db_table = 'index'

    def __str__(self):
        return '[{} - {}] {}'.format(self.index_name, self.date, self.number)
