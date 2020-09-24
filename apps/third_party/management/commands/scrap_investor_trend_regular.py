from django.core.management import BaseCommand

from apps.third_party.database.collections.investor_trend import investor_trend_register
from apps.third_party.scrap.module.scrap_investor_trend import Scrap_InvestorTrend


class Command(BaseCommand):
    help = '투자동향 저장하기'

    def add_arguments(self, parser):
        parser.add_argument('market', type = str, nargs = '?', default = '1',
                            help = 'Kospi(1)? Kosdaq(2)?')
        parser.add_argument('page_no', type = int, nargs = '?', default = 1,
                            help = 'Scrap Page No')

    def handle(self, *args, **options):
        market = options['market']
        page_no = options['page_no']

        scrap = Scrap_InvestorTrend()
        trend_data = scrap.scrap(market, page_no)
        investor_trend_register(market, trend_data)
