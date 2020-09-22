import math
import traceback
import FinanceDataReader as fdr

from apps.model.industries import Industries
from apps.model.sectors import Sectors
from apps.model.stocks import Stocks
from django.core.management import BaseCommand

from apps.third_party.util.colorful import print_green, print_yellow, print_red


class Command(BaseCommand):
    help = '한국거래소 상장 주식, 섹터, 산업 등록'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print_green('주식 정보를 가져옵니다.')
        krx = fdr.StockListing('KRX')

        for symbol, market, name, sector, industry, *_ in krx.values:
            try:
                # 보통주
                if not is_preferred_stock(sector, industry):
                    register_stock(market, symbol, name, sector, industry)

                # 우선주
                else:
                    pass

            except:
                print_red(traceback.format_exc())
                break


def is_preferred_stock(sector, industry) -> bool:
    if isinstance(sector, float) and isinstance(industry, float):
        if math.isnan(sector) and math.isnan(industry):
            return True

    return False


def register_stock(market, symbol, name, sector, industry) -> bool:
    try:
        Stocks.objects.get(stock_code = symbol)

    except Stocks.DoesNotExist:
        print_yellow('[{}] {}({}) 등록.'.format(market, name, symbol))
        sectors = register_sector(sector)
        industries = register_industry(industry)

        Stocks.objects.create(
            stock_market = market,
            stock_code = symbol,
            stock_name = name,
            sectors_id = sectors,
            industries_id = industries,
        )

    return True


def register_sector(sector) -> Sectors:
    try:
        result = Sectors.objects.get(sector_name = sector)

    except Sectors.DoesNotExist:
        result = Sectors.objects.create(
            sector_name = sector
        )

    return result


def register_industry(industry) -> Industries:
    try:
        result = Industries.objects.get(industry_name = industry)

    except Industries.DoesNotExist:
        result = Industries.objects.create(
            industry_name = industry
        )

    return result
