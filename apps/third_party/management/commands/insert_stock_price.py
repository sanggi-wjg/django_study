from django.core.management import BaseCommand

from apps.third_party.fdr.finance_data_stock_price import FinanceDataStockPrice


class Command(BaseCommand):
    help = '주가 저장'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        fd = FinanceDataStockPrice()
        fd.register()
