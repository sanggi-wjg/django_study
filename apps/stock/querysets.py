from django.db import models


class ItemsQuerySet(models.QuerySet):

    def _get_code(self, code: str):
        return self.get(code = code)
