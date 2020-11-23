from django.db import models

from apps.model.reports_name import ReportsName


class Reports(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')

    report_id = models.ForeignKey(ReportsName, on_delete = models.DO_NOTHING, db_column = 'report_id')
    number = models.FloatField(null = False, db_column = 'number')
    date = models.DateField(null = False, db_column = 'date')

    class Meta:
        managed = False
        db_table = 'reports'
