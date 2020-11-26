from django.db import models

from apps.model.reports_name import ReportsName


class ReportsQuerySet(models.QuerySet):

    def get_report_df(self, report_name: str, start_date: str, end_date: str):
        result = self.values('number', 'date').filter(
            report_id = ReportsName.objects.get(reports_name = report_name),
            date__gte = start_date, date__lte = end_date
        )

        return result


class Reports(models.Model):
    objects = ReportsQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    report_id = models.ForeignKey(ReportsName, on_delete = models.DO_NOTHING, db_column = 'report_id')
    number = models.FloatField(null = False, db_column = 'number')
    date = models.DateField(null = False, db_column = 'date')

    class Meta:
        managed = False
        db_table = 'reports'
