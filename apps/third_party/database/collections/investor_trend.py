from apps.third_party.database.mongo_db import MongoDB

COLLECTION_NAME = 'investor_trend'


def investor_trend_register(market: str, trend_data: dict):
    mongo = MongoDB()
    result = []

    try:
        for date, trend in trend_data.items():
            fs = mongo.find_one(COLLECTION_NAME, { 'market': market, 'date': date })

            if not fs:
                # 대상   O       O         X        O      O      O      O        O      O         O           O
                #        0       1         2      3      4       5       6      7       8         9            10
                #    ['개인', '외국인', '기관계', '증권', '보험', '투신', '은행', '종금', '연기금', '사모펀드', '기타법인']
                document_id = mongo.create(COLLECTION_NAME, {
                    'market'        : market,
                    'date'          : date,
                    'personal'      : trend[0],
                    'foreigner'     : trend[1],
                    'invest_firm'   : trend[3],
                    'insurance_firm': trend[4],
                    'trust_firm'    : trend[5],
                    'bank_firm'     : trend[6],
                    'non_bank_firm' : trend[7],
                    'pension_fund'  : trend[8],
                    'samo_fund'     : trend[9],
                    'etf_firm'      : trend[10],
                })
                result.append(document_id)
    finally:
        mongo.close()

    return result
