import FinanceDataReader as fdr

from django.core.management import BaseCommand

from apps.model.index import Index
from apps.third_party.util.colorful import print_green
from apps.third_party.util.utils import today_dateformat


class Command(BaseCommand):
    help = 'Register Indexes'

    def add_arguments(self, parser):
        parser.add_argument('index', type = str, help = 'Index Name... [KOSPI(KS11), KOSDAQ, ...]')
        parser.add_argument('date', type = str, nargs = '?', default = '',
                            help = 'Date to request (optional : If None, value will be today date format)')

    def handle(self, *args, **options):
        """
        python manage.py register_index KS11 all
        python manage.py register_index IXIC all
        python manage.py register_index DJI all
        python manage.py register_index US500 all
        """
        index_name = options['index'].upper()
        if options['date'] == 'all':
            start_date = '1970-01-01'
        else:
            start_date = today_dateformat(time_format = '%Y-%m-%d')

        register(index_name, start_date)


def convert_index_name(index_name):
    return {
        'KS11'   : 'KOSPI',
        'IXIC'   : 'NASDAQ',
        'DJI'    : 'DowJones',
        'US500'  : 'S&P500',
        'CL'     : 'WTI',
        'ZG'     : 'GOLD',
        'USD/KRW': 'USDKRW',
    }[index_name]


def register(index_name: str, start_date: str):
    index_df = fdr.DataReader(index_name, start_date)
    index_name = convert_index_name(index_name)

    for date, row in index_df.iterrows():
        try:
            Index.objects.get(index_name = index_name, date = date)

        except Index.DoesNotExist:
            print_green('[{} - {}] {}'.format(index_name, date, row['Close']))
            Index.objects.create(
                index_name = index_name,
                number = row['Close'],
                date = date
            )
