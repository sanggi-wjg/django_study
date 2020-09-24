import time

import pandas as pd
import numpy as np

from apps.third_party.scrap.scrap_module import ScrapModule
from apps.third_party.util.colorful import print_yellow


class Scrap_InvestorTrend(ScrapModule):

    def get_scrap_data(self):
        return self.driver.find_element_by_class_name('indx_list_ty1').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    # def parse_scrap_data(self, scrap_data):
    #     trend_list, dates = [], []
    #
    #     for d in scrap_data:
    #         date, *trend = d.text.replace(',', '').split(' ')
    #         dates.append(date.replace('/', '-'))
    #         trend_list.append(trend)
    #
    #     dataframe = pd.DataFrame(trend_list, index = dates, columns = ['개인', '외국인', '기관계', '증권', '보험', '투신', '은행', '종금', '연기금', '사모펀드', '기타법인'])
    #     return dataframe

    def parse_scrap_data(self, scrap_data):
        trend_list = { }

        for d in scrap_data:
            date, *trend = d.text.replace(',', '').split(' ')
            trend_list.setdefault(date.replace('/', '-'), trend)

        return trend_list

    def _to_dict(self, scrap_data_list):
        pass

    def scrap(self, market: str = '1', page_no: int = 1) -> dict:
        """
        :param market: 1:KOSPI / 2:KOSDAQ
        :param page_no
        """
        scrap_result = { }
        try:
            for page in range(1, page_no + 1):
                print_yellow('{} 페이지 수집 중...'.format(page))
                self.driver.get('http://stock.hankyung.com/apps/stockinfo.investor_day?market={}&page={}'.format(market, page))
                time.sleep(3)

                scrap_data = self.get_scrap_data()
                scrap_result.update(self.parse_scrap_data(scrap_data))

        except Exception as e:
            raise e
        finally:
            self.driver.quit()

        return scrap_result
