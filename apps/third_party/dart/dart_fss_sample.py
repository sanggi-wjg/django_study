import dart_fss as dart

from apps.third_party.dart.dart_settings import API_KEY

CORP_CODE = '005930'

dart.set_api_key(API_KEY)
corp_list = dart.get_corp_list()

corp_info = corp_list.find_by_corp_code(corp_code = CORP_CODE)
financial_reports = dart.fs.extract(corp_code = CORP_CODE, bgn_de = '20160101')
