from django.db import models


class Sectors(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')

    sector_name = models.CharField(max_length = 50, unique = True, db_column = 'sector_name')

    class Meta:
        managed = True
        db_table = 'sectors'
