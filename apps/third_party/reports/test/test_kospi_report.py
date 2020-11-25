import pandas as pd
import pytest

from apps.model.index import Index
from apps.model.reports import Reports
from apps.model.reports_name import ReportsName
from apps.third_party.plot.plt_utils import show_plot_twinx_list, show_plot_twinx
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

    ci_standard_df = pd.DataFrame(columns = ['CI_AVG'])
    ci_standard_df['CI_AVG'] = (ci_precede_report_df['CI_Precede'] + ci_accompany_report_df['CI_Accompany']) / 2
    ci_mean = ci_standard_df.mean(axis = 0)
    ci_std = ci_standard_df.std(axis = 0)
    ci_standard_df['CI_STANDARD'] = (ci_standard_df['CI_AVG'] - ci_mean['CI_AVG']) / ci_std['CI_AVG']

    kospi_standard_df = pd.DataFrame(columns = ['KOSPI_STANDARD'])
    kospi_mean = kospi_index_df.mean(axis = 0)
    kospi_std = kospi_index_df.std(axis = 0)
    kospi_standard_df['KOSPI_STANDARD'] = (kospi_index_df['KOSPI'] - kospi_mean['KOSPI']) / kospi_std['KOSPI']
    # print(kospi_standard_df.tail(n = 20))

    # show_plot_twinx_list(
    #     df_1 = [ci_precede_report_df, ci_accompany_report_df], df_1_label = ['경기종합지수_선행', '경기종합지수_동행'], df_1_y_label = '경기종합지수',
    #     df_2 = [kospi_index_df], df_2_label = ['KOSPI'], df_2_y_label = 'KOSPI'
    # )

    show_plot_twinx(ci_standard_df['CI_STANDARD'], '경기종합지수', kospi_standard_df['KOSPI_STANDARD'], '코스피')
