import FinanceDataReader as fdr

from apps.model.etfs import Etfs
from django.core.management import BaseCommand

from apps.model.etfs_company import EtfsCompany
from apps.third_party.util.colorful import print_green, print_yellow


class Command(BaseCommand):
    help = '한국거래소 상장 ETF 등록'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print_green('ETF 정보를 가져옵니다.')
        etf = fdr.EtfListing('KR')

        for symbol, name, *_ in etf.values:
            company_name, *etf_name = name.split(' ')
            register_etf(symbol, company_name, ''.join(etf_name))


def register_etf_company(company_name) -> EtfsCompany:
    try:
        result = EtfsCompany.objects.get(company_name = company_name)

    except EtfsCompany.DoesNotExist:
        result = EtfsCompany.objects.create(
            company_name = company_name
        )

    return result


def register_etf(etf_code: str, company_name: str, etf_name: str) -> bool:
    try:
        Etfs.objects.get(etf_code = etf_code)

    except Etfs.DoesNotExist:
        print_yellow('{} {}({}) 등록.'.format(company_name, etf_name, etf_code))
        etf_company = register_etf_company(company_name)

        Etfs.objects.create(
            etf_code = etf_code,
            etf_name = etf_name,
            company_id = etf_company
        )

    return True
