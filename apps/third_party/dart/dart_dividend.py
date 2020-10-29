import requests

from apps.third_party.dart.dart_settings import DART_API_KEY


def sample_func():
    url = '	https://opendart.fss.or.kr/api/hyslrChgSttus.json?crtfc_key={}&corp_code={}&bsns_year={}&reprt_code={}'.format(
        DART_API_KEY, '00126380', '2020', '11012'
    )

    response = requests.get(url)
    print(response.json())


sample_func()
