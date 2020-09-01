import time

from apps.third_party.scrap.chrome_driver import ChromeDriver


class ScrapModule(ChromeDriver):

    def get_scrap_data(self):
        raise NotImplementedError('get_scrap_data() is not implemented')

    def parse_scrap_data(self, scrap_data):
        raise NotImplementedError('parse_scrap_data() is not implemented')

    def _to_dict(self, scrap_data_list):
        raise NotImplementedError('_to_dict() is not implemented')

    def scrap(self, url, sleep_time = 3):

        try:
            self.driver.get(url)
            time.sleep(sleep_time)

            scrap_data = self.get_scrap_data()
            result = self.parse_scrap_data(scrap_data)
            return result

        except Exception as e:
            raise e

        finally:
            self.driver.quit()
