import requests

from apps.model.naver import Naver
from apps.model.naver_news import NaverNews
from apps.model.stocks import Stocks


class RequestNaverNews:

    def __init__(self):
        self.client_id, self.client_key = Naver.objects.get_id_n_key()

    def _request(self, keyword: str, display: int):
        try:
            Stocks.objects.get(stock_name = keyword)
        except Stocks.DoesNotExist:
            raise Stocks.DoesNotExist('{} does not exist'.format(keyword))

        response = requests.get(
            url = 'https://openapi.naver.com/v1/search/news.json?query={}&display={}'.format(keyword, display),
            headers = {
                'User-Agent'           : 'User-Created/1.0.0',
                'Accept'               : '*/*',
                'Connection'           : 'keep-alive',
                'X-Naver-Client-Id'    : self.client_id,
                'X-Naver-Client-Secret': self.client_key,
            }
        )

        return response.json()['items']

    def parse_string_news(self, stock_name: str):
        response = self._request(stock_name, 10)
        result = ''
        for item in response:
            result += '{} ({})\n'.format(escape_html_tag(item['title']), item['link'])

        return result

    def register_news(self, stock_name: str):
        response = self._request(stock_name, 100)
        for item in response:
            NaverNews.objects.register(stock_name, escape_html_tag(item['title']), item['link'], item['description'], item['pubDate'])

        return True


def escape_html_tag(text: str):
    text = text.replace('<b>', '')
    text = text.replace('</b>', '')
    text = text.replace('<br>', '')
    text = text.replace('</br>', '')
    text = text.replace('&quot;', "'")
    return text
