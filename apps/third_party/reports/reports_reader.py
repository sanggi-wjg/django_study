import os
from abc import ABCMeta, abstractmethod

from apps.model.reports_name import ReportsName
from sample.settings import INDEX_FILE_ROOT


class ReportReaderData(object):
    @property
    def data(self):
        return {
            'ICSA': ('미국 주간 실업수당 청구건수', os.path.join(INDEX_FILE_ROOT, '20201123_ICSA.csv')),
        }


class ReportReader(metaclass = ABCMeta):
    report_type = ''

    def __init__(self):
        if not self.report_type:
            raise ValueError('self report_type is empty')
        rd = ReportReaderData().data

        try:
            self.report_name = rd[self.report_type][0]
            self.ReportsName = ReportsName.objects.get(reports_name = self.report_name)

        except (KeyError, ValueError):
            raise ValueError('Invalid report_type')
        except ReportsName.DoesNotExist:
            raise ValueError('ReportsName DoesNotExist')

        try:
            self.filepath = rd[self.report_type][1]
            if not os.path.exists(self.filepath):
                raise FileNotFoundError

        except (KeyError, ValueError):
            raise ValueError('Invalid filepath')
        except FileNotFoundError:
            raise FileNotFoundError('filepath is not exist')

    @abstractmethod
    def read(self) -> list:
        raise NotImplementedError('read not implemented')

    @abstractmethod
    def save(self, read_list: list) -> bool:
        raise NotImplementedError('save not implemented')

    def register(self) -> bool:
        read_list = self.read()
        self.save(read_list)

        return True
