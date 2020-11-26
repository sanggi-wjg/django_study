from django.core.management import BaseCommand

from apps.third_party.reports.reports_creator import ReportsCreator


class Command(BaseCommand):
    help = 'Test'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        reports = ReportsCreator()

        reports.make([
            ('INDEX', 'KOSPI', 'KOSPI'),
            ('INDEX', 'NASDAQ', 'NASDAQ'),
            ('REPORT', 'CI_ACCOMPANY', '경기종합지수'),
        ], standard_normalization = True)
