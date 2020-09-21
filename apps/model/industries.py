from django.db import models


class Industries(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')

    industry_name = models.CharField(max_length = 200, unique = True, db_column = 'industry_name')

    class Meta:
        managed = False
        db_table = 'industries'
