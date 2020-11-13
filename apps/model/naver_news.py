from django.db import models

from apps.model.stocks import Stocks


class NaverNewsQuerySet(models.QuerySet):

    def register(self, stocks_name: str, title: str, link: str, description: str, pub_date: str):
        try:
            self.get(title = title)

        except NaverNews.DoesNotExist:
            self.create(
                title = title,
                link = link,
                description = description,
                pub_date = pub_date,
                stocks_id = Stocks.objects.get(stock_name = stocks_name),
            )


class NaverNews(models.Model):
    objects = NaverNewsQuerySet.as_manager()

    id = models.AutoField(primary_key = True, db_column = 'id')
    stocks_id = models.ForeignKey(Stocks, on_delete = models.DO_NOTHING, db_column = 'stocks_id')

    title = models.CharField(max_length = 200, null = False, db_column = 'title')
    link = models.CharField(max_length = 200, null = False, db_column = 'link')
    description = models.CharField(max_length = 200, null = False, db_column = 'description')
    pub_date = models.DateTimeField(null = False, db_column = 'pub_date')

    class Meta:
        managed = False
        db_table = 'naver_news'
