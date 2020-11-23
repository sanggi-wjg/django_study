import pandas as pd
import pytest

from apps.model.index import Index
from apps.model.reports import Reports
from apps.model.reports_name import ReportsName
from apps.third_party.plot.plt_utils import show_plot


@pytest.mark.django_db
def test_report():
    START_DATE = '2000-01-01'
    FINISH_DATE = '2019-12-31'

    unempl_request = Reports.objects.values('number', 'date').filter(
        report_id = ReportsName.objects.get(reports_name = '미국 주간 실업수당 청구건수'),
        date__gte = START_DATE, date__lte = FINISH_DATE
    ).order_by('date')
    index = Index.objects.all()
    kopsi = index.values('number', 'date').filter(index_name = 'KOSPI', date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
    nasdaq = index.values('number', 'date').filter(index_name = 'NASDAQ', date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')

    print()
    print(len(unempl_request), len(kopsi))
    print(unempl_request)
    print(kopsi)

    unempl_df = pd.DataFrame([x['number'] for x in unempl_request], index = [x['date'] for x in unempl_request], columns = ['UnEmployee_Request'])
    kospi_df = pd.DataFrame([x['number'] for x in kopsi], index = [x['date'] for x in kopsi], columns = ['KOSPI'])
    nasdaq_df = pd.DataFrame([x['number'] for x in nasdaq], index = [x['date'] for x in nasdaq], columns = ['NASDAQ'])

    show_plot(kospi_df, unempl_df, nasdaq_df)
