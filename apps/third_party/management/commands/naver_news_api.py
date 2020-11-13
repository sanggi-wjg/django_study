from django.core.management import BaseCommand

from apps.model.stock_subs import StockSubs
from apps.third_party.naver.request_naver import RequestNaverNews


class Command(BaseCommand):
    help = 'Scrap Naver News'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        request_naver = RequestNaverNews()

        for stock in get_subs_stock_list():
            request_naver.register_news(stock['stocks_id__stock_name'])


def get_subs_stock_list():
    stock_list = StockSubs.objects.values('stocks_id__stock_name').all()
    return stock_list
