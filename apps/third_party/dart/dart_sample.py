import requests

from apps.third_party.dart.dart_settings import API_KEY

reprt_code = [
    '11011',  # 사업보고서
    '11012',  # 반기보고서
    '11013',  # 1분기 보고서
    '11014',  # 사업보고서
]
fs_div = [
    'OFS',  # 재무제표
    'CFS',  # 연결 제무제표
]


def request_dart(corp_code, year):
    request_url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={0}&corp_code={1}&bsns_year={2}&reprt_code={3}&fs_div={4}'.format(
        API_KEY, corp_code, year, report_code[0], fs_div[0]
    )

    response = requests.get(request_url)
    print(response.json())


if __name__ == '__main__':
    request_dart('005930', '2019')
