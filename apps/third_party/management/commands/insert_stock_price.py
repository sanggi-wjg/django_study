from django.core.management import BaseCommand
from django.db.models import Count, F

from apps.model.portfolios_detail import PortfoliosDetail
from apps.third_party.fdr.finance_data_stock_price import FinanceDataStockPrice


class Command(BaseCommand):
    help = '주가 저장'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        fd = FinanceDataStockPrice()

        for stock in _get_stock_list():
            fd.register(stock['stocks_id'], stock['stocks_id__stock_code'], stock_name = stock['stocks_id__stock_name'])


def _get_stock_list():
    return PortfoliosDetail.objects.values(
        'stocks_id__stock_code', 'stocks_id__stock_name'
    ).annotate(
        stock_count = Count('stocks_id'),
        stocks_id = F('stocks_id'),
    )
