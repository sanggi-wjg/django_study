from django.db import models


class ApiListQuerySet(models.QuerySet):

    def get_one(self, api_name: str):
        result = self.values(
            'api_name', 'api_id', 'api_key', 'api_url'
        ).get(
            api_name = api_name
        )
        return result


class ApiList(models.Model):
    """
    폐기물 https://www.recycling-info.or.kr/

    """
    objects = ApiListQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')

    api_name = models.CharField(max_length = 50, null = False, db_column = 'api_name')
    api_id = models.CharField(max_length = 50, null = False, db_column = 'api_id')
    api_key = models.CharField(max_length = 100, null = False, db_column = 'api_key')
    api_url = models.CharField(max_length = 100, null = False, db_column = 'api_url')

    class Meta:
        managed = False
        db_table = 'api_list'
