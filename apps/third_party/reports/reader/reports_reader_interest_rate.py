from openpyxl import load_workbook

from apps.third_party.reports.reader.reports_reader import ReportReader


class ReportsReader_InterestRate(ReportReader):
    report_type = 'INTEREST_RATE'

    def read(self) -> list:
        workbook = load_workbook(filename = self.filepath, read_only = True, data_only = True)
        try:
            read_list = []
            sheet = workbook.worksheets[0]

            for no, row in enumerate(sheet.iter_rows(values_only = True)):
                if no == 0: continue
                """
                국고채3년(평균)	국고채5년(평균)	국고채10년(평균)	회사채3년(평균)	CD91물(평균)	콜금리(1일물,평균)	기준금리
                (1999, '04월', 6.37, 7.09, '-', 7.56, 6.16, 4.81, '-')
                (1999, '05월', 6.75, 7.97, '-', 8.32, 6.17, 4.78, 4.75)
                """
                interest_rate = row[8]

                if interest_rate != '-':
                    read_list.append({
                        'date'  : '{}-{}-01'.format(row[0], row[1].replace('월', '')),
                        'number': interest_rate,
                    })
        finally:
            workbook.close()

        return read_list
