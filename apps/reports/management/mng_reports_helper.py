from apps.third_party.reports.reader.reports_reader import ReportReader


def create_reader(report_reader: str) -> ReportReader:
    if report_reader == 'ICSA':
        from apps.third_party.reports.reader.reports_reader_icsa import ReportsReader_ICSA
        return ReportsReader_ICSA()

    elif report_reader == 'CI_PRECEDE':
        from apps.third_party.reports.reader.reports_reader_composite_index import ReportsReader_CompositeIndex_Precede
        return ReportsReader_CompositeIndex_Precede()

    elif report_reader == 'CI_ACCOMPANY':
        from apps.third_party.reports.reader.reports_reader_composite_index import ReportsReader_CompositeIndex_Accompany
        return ReportsReader_CompositeIndex_Accompany()

    elif report_reader == 'INTEREST_RATE':
        from apps.third_party.reports.reader.reports_reader_interest_rate import ReportsReader_InterestRate
        return ReportsReader_InterestRate()

    else:
        raise ValueError('report_reader Not Allowed')
