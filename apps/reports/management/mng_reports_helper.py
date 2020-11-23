from apps.third_party.reports.reports_reader import ReportReader
from apps.third_party.reports.reports_reader_icsa import ReportsReader_ICSA


def create_reader(report_reader: str) -> ReportReader:
    if report_reader == 'ICSA':
        return ReportsReader_ICSA()
    else:
        raise ValueError('report_reader not allowed')
