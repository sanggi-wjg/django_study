from django.core.management import BaseCommand
from django.db.models import Count, F

from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stocks import Stocks
from apps.third_party.fdr.finance_data_stock_price import FinanceDataStockPrice
from apps.third_party.util.colorful import print_red


class Command(BaseCommand):
    help = '주가 저장'

    def add_arguments(self, parser):
        parser.add_argument('stock_code', type = str, nargs = '?', default = None,
                            help = 'Stock Code')

    def handle(self, *args, **options):
        fd = FinanceDataStockPrice()

        if options['stock_code'] is None:
            for stock in _get_stock_list():
                try:
                    fd.register(stock['stocks_id'], stock['stocks_id__stock_code'], stock_name = stock['stocks_id__stock_name'])
                    # fd.register(stock['id'], stock['stock_code'], stock_name = stock['stock_name'])
                except:
                    continue
        else:
            try:
                stock = Stocks.objects.values('id', 'stock_code', 'stock_name').get(stock_code = options['stock_code'])
                fd.register(stock['id'], stock['stock_code'], stock_name = stock['stock_name'])
            except Stocks.DoesNotExist:
                print_red('Invalid stock_code : {}'.format(options['stock_code']))


def _get_stock_list():
    return PortfoliosDetail.objects.values(
        'stocks_id__stock_code', 'stocks_id__stock_name'
    ).annotate(
        stock_count = Count('stocks_id'),
        stocks_id = F('stocks_id'),
    )
    # return Stocks.objects.values('stock_code', 'stock_name', 'id').all()
