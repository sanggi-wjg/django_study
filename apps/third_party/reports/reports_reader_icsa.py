import csv

from apps.model.reports import Reports
from apps.third_party.reports.reports_reader import ReportReader


class ReportsReader_ICSA(ReportReader):
    report_type = 'ICSA'

    def read(self) -> list:
        file = open(self.filepath, 'r', encoding = 'utf-8')
        try:
            lines = csv.reader(file)
            read_list = [{
                'date'  : str(x[0]),
                'number': int(x[1]),
            } for x in lines]
        finally:
            file.close()

        return read_list

    def save(self, read_list: list) -> bool:

        for read in read_list:
            try:
                Reports.objects.get(date = read['date'], report_id = self.ReportsName)

            except Reports.DoesNotExist:
                Reports.objects.create(
                    report_id = self.ReportsName,
                    date = read['date'],
                    number = read['number'],
                )

        return True
