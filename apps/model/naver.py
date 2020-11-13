from django.db import models


class NaverQuerySet(models.QuerySet):

    def get_id_n_key(self):
        result = self.get(id = 1)
        return result.client_id, result.client_key


class Naver(models.Model):
    objects = NaverQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')
    client_id = models.CharField(max_length = 50, null = False, db_column = 'client_id')
    client_key = models.CharField(max_length = 50, null = False, db_column = 'client_key')

    class Meta:
        managed = False
        db_table = 'naver'
