import traceback

from django.core.management import BaseCommand

from apps.model.stocks import Stocks
from apps.third_party.database.collections.demand import demand_info_register
from apps.third_party.scrap.module.scrap_demand import Scrap_Demand


class Command(BaseCommand):
    help = '등록된 주식회사 수급정보 저장하기'

    def add_arguments(self, parser):
        parser.add_argument('stock_code', type = str, nargs = '?', default = '',
                            help = 'Stock Code')

    def handle(self, *args, **options):
        stock_items = Stocks.objects.values('stock_code', 'stock_name').all()

        for stock in stock_items:
            try:
                print('[{}] {} demand scraping...'.format(stock['stock_code'], stock['stock_name']))
                request_scrap(stock['stock_code'])
            except:
                print(traceback.format_exc())
                continue


def request_scrap(stock_code: str):
    scrap = Scrap_Demand()
    scrap_data = scrap.scrap('https://finance.daum.net/quotes/A{stock_code}#influential_investors/home'.format(stock_code = stock_code))
    demand_info_register(stock_code, demand_data = scrap_data)
