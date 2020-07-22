import time

from selenium import webdriver


class ScrapMain:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(executable_path = '/home/django_sample/apps/third_party/scrap/chromedriver', options = options)

    def get_scrap_data(self):
        raise NotImplementedError('get_scrap_data() is not implemented')

    def parse_scrap_data(self, scrap_data):
        raise NotImplementedError('parse_scrap_data() is not implemented')

    def _to_dict(self, scrap_data_list):
        raise NotImplementedError('_to_dict() is not implemented')

    def run(self, url, sleep_time = 3):

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
