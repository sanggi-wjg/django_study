import traceback

from django.core.management import BaseCommand

from apps.stock.models import Items
from apps.third_party.database.collections.demand import Mongo_Demand
from apps.third_party.scrap.module.scrap_demand import Scrap_Demand


class Command(BaseCommand):
    help = '등록된 주식회사 수급정보 저장하기'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        stock_items = Items.objects.values('code', 'name').all()

        for stock in stock_items:
            try:
                print('[{}] {} demand scraping...'.format(stock['code'], stock['name']))
                request_scrap(stock['code'])

            except:
                print(traceback.format_exc())
                continue


def request_scrap(stock_code: str):
    scrap = Scrap_Demand()
    scrap_data = scrap.scrap('https://finance.daum.net/quotes/A{stock_code}#influential_investors/home'.format(stock_code = stock_code))
    Mongo_Demand().query('register', stock_items_code = stock_code, demand_data = scrap_data)
