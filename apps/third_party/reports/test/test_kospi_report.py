import pandas as pd
import pytest

from apps.model.index import Index
from apps.model.reports import Reports
from apps.model.reports_name import ReportsName
from apps.third_party.plot.plt_utils import show_plot_twinx_list
from apps.third_party.reports.reader.reports_reader import ReportReaderData


@pytest.mark.django_db
def test_kospi():
    START_DATE, FINISH_DATE = '{}-01-01'.format(1990), '{}-12-31'.format(2020)

    ci_report = Reports.objects.values('number', 'date').filter(
        date__gte = START_DATE, date__lte = FINISH_DATE
    ).order_by('date')
    ci_precede_report = ci_report.filter(report_id = ReportsName.objects.get(reports_name = ReportReaderData().data['CI_PRECEDE'][0]))
    ci_accompany_report = ci_report.filter(report_id = ReportsName.objects.get(reports_name = ReportReaderData().data['CI_ACCOMPANY'][0]))

    kopsi_index = Index.objects.values('number', 'date').filter(index_name = 'KOSPI', date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')

    ci_precede_report_df = pd.DataFrame([x['number'] for x in ci_precede_report], index = [x['date'] for x in ci_precede_report], columns = ['CI_Precede'])
    ci_accompany_report_df = pd.DataFrame([x['number'] for x in ci_accompany_report], index = [x['date'] for x in ci_accompany_report], columns = ['CI_Accompany'])
    kospi_index_df = pd.DataFrame([x['number'] for x in kopsi_index], index = [x['date'] for x in kopsi_index], columns = ['KOSPI'])

    show_plot_twinx_list(
        df_1 = [ci_precede_report_df, ci_accompany_report_df], df_1_label = ['경기종합지수_선행', '경기종합지수_동행'], df_1_y_label = '경기종합지수',
        df_2 = [kospi_index_df], df_2_label = ['KOSPI'], df_2_y_label = 'KOSPI'
    )
