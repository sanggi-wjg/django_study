from django.db import models


class ReportsNameQuerySet(models.QuerySet):

    def find(self, reports_name: str):
        pass


class ReportsName(models.Model):
    objects = ReportsNameQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')
    reports_name = models.CharField(max_length = 100, null = False, db_column = 'reports_name')

    class Meta:
        managed = False
        db_table = 'reports_name'
