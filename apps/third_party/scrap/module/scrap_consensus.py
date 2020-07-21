from apps.third_party.scrap.scrap_main import ScrapMain
from apps.third_party.scrap.scrap_util import escape_number


class Scrap_Consensus(ScrapMain):

    def get_scrap_data(self):
        self.driver.switch_to.frame('frmFS1')
        return self.driver.find_element_by_id('cTB25').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    def parse_scrap_data(self, scrap_data):
        result = []

        for d in scrap_data:
            text_to_list = d.text.split(' ')
            if len(text_to_list) >= 1:
                if self._is_year_number(text_to_list[0]):
                    result.append(text_to_list)

        return self._parse_to_dict(result)

    @staticmethod
    def _parse_to_dict(scrap_data_list):
        result = []

        for i, data in enumerate(scrap_data_list):
            result.append({
                'year'           : str(data[0]),
                'total_sales'    : int(escape_number(data[2])),
                'total_sales_yoy': float(escape_number(data[3])),
                'business_profit': int(escape_number(data[4])),
                'net_profit'     : int(escape_number(data[5])),
                'eps'            : int(escape_number(data[6])),
                'per'            : float(escape_number(data[7])),
                'pbr'            : float(escape_number(data[8])),
                'roe'            : float(escape_number(data[9])),
                'evebitda'       : float(escape_number(data[10])),
                'debt_ratio'     : float(escape_number(data[11])),
            })

        return result

    @staticmethod
    def _is_year_number(text):
        try:
            text = int(text.replace('(A)', '').replace('(E)', ''))
        except ValueError:
            return False

        if isinstance(text, int):
            return True

        return False
