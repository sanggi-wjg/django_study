from apps.third_party.scrap.scrap_module import ScrapModule
from apps.third_party.util.utils import escape_number


class Scrap_Consensus(ScrapModule):

    def get_scrap_data(self):
        self.driver.switch_to.frame('frmFS1')
        return self.driver.find_element_by_id('cTB25').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    def parse_scrap_data(self, scrap_data):
        result = []

        for d in scrap_data:
            to_list = d.text.split(' ')
            if len(to_list) > 2:
                if self._is_year_number(to_list[0]):
                    result.append(to_list)

        return self._to_dict(result)

    def _to_dict(self, scrap_data_list):
        result = []

        for i, data in enumerate(scrap_data_list):
            if len(data) != 12:
                data.insert(2, '0')
                data.insert(3, '0')
                data.insert(10, '0')
                data.insert(11, '0')

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
