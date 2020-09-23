import time

from apps.third_party.scrap.chrome_driver import ChromeDriver


class ScrapETF(ChromeDriver):
    ETF_NAME = 'QQQ'
    URL = 'https://www.etf.com'

    def _access(self):
        self.driver.get('{}/{}'.format(self.URL, self.ETF_NAME))
        time.sleep(5)

    def _get_overview(self) -> list:
        overview = self.driver.find_element_by_id('form-reports-header')
        etf_name = overview.find_elements_by_tag_name('span')[0]
        etf_rating_letter, etf_rating_score, *_ = overview.find_element_by_class_name('overallScore').find_element_by_class_name('display-table-cell').find_elements_by_tag_name('div')

        return [('etf_name', etf_name.text), ('etf_rating_letter', etf_rating_letter.text), ('etf_rating_score', etf_rating_score.text)]

    def _get_summary(self) -> list:
        summaries = self.driver.find_element_by_id('fundSummaryData').find_element_by_class_name('generalDataBox').find_elements_by_tag_name('div')
        result = [(tuple(summary.text.split('\n'))) for summary in summaries]

        return result

    def scrap(self):
        self._access()
        print(self._get_overview())
        print(self._get_summary())


if __name__ == '__main__':
    scrap = ScrapETF()
    scrap.scrap()
