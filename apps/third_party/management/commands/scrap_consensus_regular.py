import traceback
from multiprocessing import Pool

from django.core.management import BaseCommand

from apps.model.stocks import Stocks
from apps.third_party.database.collections.financial_info import financial_info_register
from apps.third_party.scrap.module.scrap_consensus import Scrap_Consensus
from apps.third_party.util.utils import get_cpu_count


class Command(BaseCommand):
    help = '등록된 주식회사 컨센서스 저장하기'

    def add_arguments(self, parser):
        parser.add_argument('stock_code', type = str, nargs = '?', default = None,
                            help = 'Stock Code')

    def handle(self, *args, **options):
        if options['stock_code'] is None:
            stock_list = Stocks.objects.values('stock_code', 'stock_name').all()
        else:
            stock_list = Stocks.objects.values('stock_code', 'stock_name').filter(stock_code = options['stock_code'])

        pool = Pool(processes = get_cpu_count())
        result = pool.map(request_scrap, stock_list)


def request_scrap(stock: dict):
    print('[{}] {} Consensus scraping...'.format(stock['stock_code'], stock['stock_name']))

    try:
        scrap = Scrap_Consensus()
        scrap_data = scrap.scrap('https://wisefn.finance.daum.net/company/c1010001.aspx?cmp_cd={stock_code}'.format(stock_code = stock['stock_code']))
        financial_info_register(stock['stock_code'], financial_data = scrap_data)

    except Exception:
        print(traceback.format_exc())
