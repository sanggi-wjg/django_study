from pprint import pprint

from apps.third_party.scrap.scrap_main import ScrapMain
from apps.third_party.scrap.scrap_util import escape_number, escape_char
from apps.third_party.util.time_helper import today_dateformat


class Scrap_Demand(ScrapMain):

    def get_scrap_data(self):
        return self.driver.find_element_by_class_name('box_contents').find_element_by_tag_name('div').find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    def parse_scrap_data(self, scrap_data):
        result = []

        for d in scrap_data:
            to_list = d.text.split('\n')
            result.append(to_list)

        return self._to_dict(result)

    def _to_dict(self, scrap_data_list):
        result = []

        for data in scrap_data_list:
            year = today_dateformat('%Y')

            result.append({
                'date'                   : '{}-{}'.format(year, data[0].replace('.', '-')),
                'foreign_total_own'      : int(escape_number(data[1])),
                'foreign_total_own_ratio': float(escape_char(data[2])),
                'foreign_purchase_volume': int(escape_number(data[3])),
                'company_purchase_volume': int(escape_number(data[4])),
                'closing_price'          : int(escape_number(data[5])),
                'compare_prev_day'       : str(escape_number(data[6])),
                'fluctuation_ratio'      : float(escape_char(data[7])),
            })

        pprint(result)
        return result


if __name__ == '__main__':
    scrap = Scrap_Demand()
    scrap.run('https://finance.daum.net/quotes/A055550#influential_investors/home')
