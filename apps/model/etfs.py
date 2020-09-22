from django.db import models

from apps.model.etfs_company import EtfsCompany


class Etfs(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')

    etf_code = models.CharField(max_length = 10, unique = True, null = False, db_column = 'etf_code')
    etf_name = models.CharField(max_length = 50, unique = True, null = False, db_column = 'etf_name')

    company_id = models.ForeignKey(EtfsCompany, on_delete = models.DO_NOTHING, db_column = 'company_id')

    class Meta:
        managed = False
        db_table = 'etfs'

    def __str__(self):
        return '{}({})'.format(self.etf_name, self.etf_code)
