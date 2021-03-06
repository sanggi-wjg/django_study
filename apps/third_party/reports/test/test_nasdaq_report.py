# import pandas as pd
# import pytest
#
# from apps.model.index import Index
# from apps.model.reports import Reports
# from apps.model.reports_name import ReportsName
# from apps.third_party.plot.plt_helpers import plt_year_format
# from apps.third_party.plot.plt_utils import show_plot_twinx
# from apps.third_party.reports.reader.reports_reader import ReportReaderData
#
#
# @pytest.mark.django_db
# def test_report():
#     TERM = 5
#
#     for year in range(1980, 2021, TERM):
#         START_DATE, FINISH_DATE = '{}-01-01'.format(year), '{}-12-31'.format(year + (TERM - 1))
#
#         unempl_request = Reports.objects.values('number', 'date').filter(
#             report_id = ReportsName.objects.get(reports_name = ReportReaderData().data['ICSA'][0]),
#             date__gte = START_DATE, date__lte = FINISH_DATE
#         ).order_by('date')
#
#         index = Index.objects.all()
#         kopsi = index.values('number', 'date').filter(index_name = 'KOSPI', date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
#         nasdaq = index.values('number', 'date').filter(index_name = 'NASDAQ', date__gte = START_DATE, date__lte = FINISH_DATE).order_by('date')
#
#         unempl_df = pd.DataFrame([x['number'] for x in unempl_request], index = [x['date'] for x in unempl_request], columns = ['UnEmployee_Request'])
#         kospi_df = pd.DataFrame([x['number'] for x in kopsi], index = [x['date'] for x in kopsi], columns = ['KOSPI'])
#         nasdaq_df = pd.DataFrame([x['number'] for x in nasdaq], index = [x['date'] for x in nasdaq], columns = ['NASDAQ'])
#
#         show_plot_twinx(
#             unempl_df, 'UnEmployee_Request', nasdaq_df, 'NASDAQ', plot_format = plt_year_format,
#             filedir = 'UnEmployee_Request_NASDAQ',
#             filename = '[{}_{}]_UnEmployee_Request_NASDAQ.png'.format(START_DATE, FINISH_DATE),
#         )
