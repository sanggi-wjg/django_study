from django.db import models


class DartCorpCodeQuerySet(models.QuerySet):

    def register(self, corp_code: str, corp_name: str, stock_code: str = None):
        try:
            self.get(corp_code = corp_code)

        except DartCorpCode.DoesNotExist:
            self.create(
                corp_code = corp_code,
                corp_name = corp_name,
                stock_code = stock_code
            )


class DartCorpCode(models.Model):
    objects = DartCorpCodeQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    corp_code = models.CharField(max_length = 8, unique = True, null = False, db_column = 'corp_code')
    corp_name = models.CharField(max_length = 100, null = False, db_column = 'corp_name')
    stock_code = models.CharField(max_length = 6, blank = True, null = True, db_column = 'stock_code')

    class Meta:
        managed = False
        db_table = 'dart_corp_code'

    def __str__(self):
        return '{} ({}:{})'.format(self.corp_name, self.stock_code, self.corp_code)
