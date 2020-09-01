from selenium import webdriver

from sample.settings import CHROME_DRIVER_PATH


class ChromeDriver:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH, options = options)
