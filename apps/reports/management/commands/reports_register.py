from django.core.management import BaseCommand

from apps.reports.management.mng_reports_helper import create_reader


class Command(BaseCommand):
    help = 'Test'

    def add_arguments(self, parser):
        parser.add_argument('report_type', type = str, help = 'Report Type')

    def handle(self, *args, **options):
        reader = create_reader(options['report_type'])
        reader.register()
