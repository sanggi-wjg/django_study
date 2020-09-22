from django.db import models


class EtfsCompany(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'id')

    company_name = models.CharField(max_length = 50, unique = True, null = False, db_column = 'company_name')

    class Meta:
        managed = False
        db_table = 'etfs_company'

    def __str__(self):
        return self.company_name
