import pytest
import requests

from apps.model.api_list import ApiList
from apps.third_party.database.collections.waste_report import register_waster_report


@pytest.mark.django_db
def test_api():
    api = ApiList.objects.get_one(api_name = '자원순환정보시스템 API')

    result_dic = { }

    for year in range(2019, 2021):
        req_url = '{}?PID={}&YEAR={}&USRID={}&KEY={}'.format(api['api_url'], 'NTN003', year, api['api_id'], api['api_key'])
        response = requests.get(url = req_url)
        print(response.json())
        result_dic[str(year)] = req_parse(response.json())

    register_waster_report(result_dic)


def req_parse(response):
    result = []

    for r in response['data']:
        if r.get('CITY_JIDT_NM') != '전국':
            break
        """
        "CITY_JIDT_NM": "전국"
        "DATA_TM_NM": "발생량",
        "TOT_SUM": 45008.9, 총계
        "SPEC_SUM": 19660.8, 종량제 혼합배출 소계
        "FOOD_SUM": 13401.8, 음식물 배출
        "DSTRCT_SUM": 11946.3, 재활용 분리배출
        """
        result.append({
            'DATA_TM_NM': r['DATA_TM_NM'],
            'TOT_SUM'   : r['TOT_SUM'],
            'SPEC_SUM'  : r['SPEC_SUM'],
            'FOOD_SUM'  : r['FOOD_SUM'],
            'DSTRCT_SUM': r['DSTRCT_SUM'],
        })

    return result
