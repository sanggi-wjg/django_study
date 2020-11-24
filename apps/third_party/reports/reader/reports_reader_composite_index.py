from openpyxl import load_workbook

from apps.third_party.reports.reader.reports_reader import ReportReader


class ReportsReader_CompositeIndex_Precede(ReportReader):
    """
    https://www.index.go.kr/potal/main/EachDtlPageDetail.do?idx_cd=1057
    ㅇ 경기종합지수에는 선행(Leading), 동행(Coincident), 후행(Lagging)종합지수가 있음
        (1) 선행종합지수는 앞으로의 경기동향을 예측하는 지표로서 구인구직비율, 건설수주액, 재고순환지표 등과 같이 앞으로 일어날 경제현상을 미리 알려주는 9개 지표들의 움직임을 종합하여 작성함
        (2) 동행종합지수는 현재의 경기상태를 나타내는 지표로서 광공업생산지수, 소매판매액지수, 비농림어업취업자수 등과 같이 국민경제 전체의 경기변동과 거의 동일한 방향으로 움직이는 7개 지표로 구성됨
        (3) 후행종합지수는 경기의 변동을 사후에 확인하는 지표로서 생산자제품재고지수, 회사채유통수익률, 가계소비지출 등과 같은 5개 지표로 구성됨
    """
    report_type = 'CI_PRECEDE'

    def read(self) -> list:
        workbook = load_workbook(filename = self.filepath, read_only = True, data_only = True)
        try:
            read_list = []
            sheet = workbook.worksheets[0]

            for no, row in enumerate(sheet.iter_rows(values_only = True)):
                if no == 0: continue
                """
                (1970, '01월', 100.6, None, 101, None)
                (1970, '02월', 101.5, None, 100.9, None)
                """
                read_list.append({
                    'date'  : '{}-{}-01'.format(row[0], row[1].replace('월', '')),
                    'number': row[4],
                })

        finally:
            workbook.close()

        return read_list


class ReportsReader_CompositeIndex_Accompany(ReportReader):
    report_type = 'CI_ACCOMPANY'

    def read(self) -> list:
        workbook = load_workbook(filename = self.filepath, read_only = True, data_only = True)
        try:
            read_list = []
            sheet = workbook.worksheets[0]

            for no, row in enumerate(sheet.iter_rows(values_only = True)):
                if no == 0: continue
                """
                (1970, '01월', 100.6, None, 101, None)
                (1970, '02월', 101.5, None, 100.9, None)
                """
                read_list.append({
                    'date'  : '{}-{}-01'.format(row[0], row[1].replace('월', '')),
                    'number': row[2],
                })

        finally:
            workbook.close()

        return read_list
