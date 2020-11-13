from django.core.management import BaseCommand

from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks
from apps.third_party.util.colorful import print_green, print_yellow


class Command(BaseCommand):
    help = 'test'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        price_list = StockPrice.objects.values('close_price', 'high_price', 'low_price', 'date').filter(stocks_id = Stocks.objects.get(stock_name = '삼성전자').id).order_by('-date')[:14]
        print_green(price_list)
