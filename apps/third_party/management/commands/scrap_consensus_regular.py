import traceback

from django.core.management import BaseCommand

from apps.model.stocks import Stocks
from apps.third_party.database.collections.financial_info import financial_info_register
from apps.third_party.scrap.module.scrap_consensus import Scrap_Consensus


class Command(BaseCommand):
    help = '등록된 주식회사 컨센서스 저장하기'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        stock_items = Stocks.objects.values('stock_code', 'stock_name').all()

        for stock in stock_items:
            try:
                print('[{}] {} consensus scraping...'.format(stock['stock_code'], stock['stock_name']))
                request_scrap(stock['stock_code'])

            except:
                print(traceback.format_exc())
                continue


def request_scrap(stock_code: str):
    scrap = Scrap_Consensus()
    scrap_data = scrap.scrap('https://wisefn.finance.daum.net/company/c1010001.aspx?cmp_cd={stock_code}'.format(stock_code = stock_code))
    financial_info_register(stock_code, financial_data = scrap_data)
