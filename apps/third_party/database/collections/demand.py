from apps.third_party.database.mongo_db import MongoDB

# class Mongo_Demand(MongoDAO):
#
#     @staticmethod
#     def register(mongo, stock_code, demand_data):
#         if not demand_data: raise ValueError('Empty demand_data')
#         collection_name = 'demand_info'
#         document_result = []
#
#         for data in demand_data:
#             fs = mongo.find_one(collection_name, { "stock_code": stock_code, 'date': data['date'] })
#
#             if not fs:
#                 document_id = mongo.create(collection_name, {
#                     'stock_code'             : stock_code,
#                     'date'                   : data['date'],
#                     'foreign_total_own'      : data['foreign_total_own'],
#                     'foreign_total_own_ratio': data['foreign_total_own_ratio'],
#                     'foreign_purchase_volume': data['foreign_purchase_volume'],
#                     'company_purchase_volume': data['company_purchase_volume'],
#                     'closing_price'          : data['closing_price'],
#                     'compare_prev_day'       : data['compare_prev_day'],
#                     'fluctuation_ratio'      : data['fluctuation_ratio'],
#                 })
#                 document_result.append(document_id)
#
#         return document_result

COLLECTION_NAME = 'demand_info'


def demand_info_register(stock_code: str, demand_data: dict):
    mongo = MongoDB()
    result = []

    try:
        for data in demand_data:
            fs = mongo.find_one(COLLECTION_NAME, { 'stock_code': stock_code, 'date': data['date'] })

            if not fs:
                document_id = mongo.create(COLLECTION_NAME, {
                    'stock_code'             : stock_code,
                    'date'                   : data['date'],
                    'foreign_total_own'      : data['foreign_total_own'],
                    'foreign_total_own_ratio': data['foreign_total_own_ratio'],
                    'foreign_purchase_volume': data['foreign_purchase_volume'],
                    'company_purchase_volume': data['company_purchase_volume'],
                    'closing_price'          : data['closing_price'],
                    'compare_prev_day'       : data['compare_prev_day'],
                    'fluctuation_ratio'      : data['fluctuation_ratio'],
                })
                result.append(document_id)
    finally:
        mongo.close()

    return result
