from apps.third_party.database.mongo_db import MongoDB

COLLECTION_NAME = 'waste_report'


def register_waster_report(data_dic: dict):
    mongo = MongoDB()
    result = []

    try:
        for year, item in data_dic.items():
            for data in item:
                fs = mongo.find_one(COLLECTION_NAME, { 'year': year, 'DATA_TM_NM': data['DATA_TM_NM'] })

                if not fs:
                    document_id = mongo.create(COLLECTION_NAME, {
                        'year'    : year,
                        'DATA_TM_NM': data['DATA_TM_NM'],
                        'TOT_SUM'   : data['TOT_SUM'],
                        'SPEC_SUM'  : data['SPEC_SUM'],
                        'FOOD_SUM'  : data['FOOD_SUM'],
                        'DSTRCT_SUM': data['DSTRCT_SUM'],
                    })
                    result.append(document_id)
    finally:
        mongo.close()

    return result
