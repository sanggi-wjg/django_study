from django.core.management import BaseCommand
from django.db.models import Count

from apps.model.index import Index
from apps.model.reports import Reports
from apps.third_party.reports.reports_creator import ReportsCreator
from apps.third_party.util.colorful import print_yellow, print_red


class Command(BaseCommand):
    help = 'Test'

    def add_arguments(self, parser):
        parser.add_argument('debug', type = str, nargs = '?', default = None,
                            help = 'debug')

    def handle(self, *args, **options):
        if options['debug']:
            show_list()

        targets = [
            ['INDEX', 'KOSPI', 'KOSPI'],
            # ['INDEX', 'NASDAQ', 'NASDAQ'],
            # ['REPORT', 'CI_ACCOMPANY', '경기종합지수'],
            ['INDEX', 'GOLD', '금'],
            # ['INDEX', 'USDKRW', '환율'],
        ]

        reports = ReportsCreator()
        reports.make(
            targets,
            filedir = get_filedir(targets),
            standard = False,
            normalization = False
        )


def get_filedir(targets):
    try:
        result = ['_'.join(x) for x in targets]
        result = '_'.join(result).replace('INDEX_', '').replace('REPORT_', '').replace('STOCK_', '')
    except Exception:
        raise ValueError('targets Is Invalid')

    if not result:
        raise ValueError('filedir Is Not Set')

    return result


def show_list():
    print_red('------ [인덱스] ------')
    index_list = Index.objects.values('index_name').annotate(count = Count('index_name'))
    for index in index_list:
        print_yellow(index['index_name'])

    print_red('------ [리포트] ------')
    report_list = Reports.objects.values('report_id__reports_name').annotate(count = Count('report_id__reports_name'))
    for report in report_list:
        print_yellow(report['report_id__reports_name'])

    print_red('----------------------')
    exit()
