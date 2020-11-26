from django.core.management import BaseCommand

from apps.third_party.reports.reports_creator import ReportsCreator


class Command(BaseCommand):
    help = 'Test'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        type_1 = [
            ('INDEX', 'KOSPI', 'KOSPI'),
            ('INDEX', 'NASDAQ', 'NASDAQ'),
            ('REPORT', 'CI_ACCOMPANY', '경기종합지수'),
        ]
        type_2 = [
            ('INDEX', 'KOSPI', 'KOSPI'),
            ('INDEX', 'NASDAQ', 'NASDAQ'),
            ('INDEX', 'USDKRW', '환율'),
        ]

        reports = ReportsCreator()
        reports.make(
            type_2,
            filedir = 'Currency',
            standard_normalization = True
        )
