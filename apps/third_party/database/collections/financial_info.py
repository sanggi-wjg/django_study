from apps.third_party.database.mongo_db import MongoDB

# class Mongo_FI(MongoDAO):
#
#     @staticmethod
#     def register(mongo, stock_code, fi_data):
#         if not fi_data: raise ValueError('Empty fi_data')
#         collection_name = 'finance_info'
#         document_result = []
#
#         for data in fi_data:
#             fs = mongo.find_one(collection_name, { "stock_code": stock_code, 'year': data['year'] })
#
#             if not fs:
#                 document_id = mongo.create(collection_name, {
#                     'stock_code'     : stock_code,
#                     'year'           : data['year'],
#                     'total_sales'    : data['total_sales'],
#                     'total_sales_yoy': data['total_sales_yoy'],
#                     'business_profit': data['business_profit'],
#                     'net_profit'     : data['net_profit'],
#                     'eps'            : data['eps'],
#                     'per'            : data['per'],
#                     'pbr'            : data['pbr'],
#                     'roe'            : data['roe'],
#                     'evebitda'       : data['evebitda'],
#                     'debt_ratio'     : data['debt_ratio'],
#                     'epsroe'         : int(data['eps'] * data['roe'])
#                 })
#                 document_result.append(document_id)
#
#             else:
#                 if '(E)' in data['year']:
#                     document_id = mongo.update_one(
#                         collection_name,
#                         document_id = { 'stock_code': stock_code, 'year': data['year'] },
#                         data = {
#                             'total_sales'    : data['total_sales'],
#                             'total_sales_yoy': data['total_sales_yoy'],
#                             'business_profit': data['business_profit'],
#                             'net_profit'     : data['net_profit'],
#                             'eps'            : data['eps'],
#                             'per'            : data['per'],
#                             'pbr'            : data['pbr'],
#                             'roe'            : data['roe'],
#                             'evebitda'       : data['evebitda'],
#                             'debt_ratio'     : data['debt_ratio'],
#                             'epsroe'         : int(data['eps'] * data['roe'])
#                         }
#                     )
#                     document_result.append(document_id)
#
#         return document_result

COLLECTION_NAME = 'finance_info'


def financial_info_register(stock_code: str, financial_data: dict):
    mongo = MongoDB()
    result = []

    try:
        for data in financial_data:
            fs = mongo.find_one(COLLECTION_NAME, { "stock_code": stock_code, 'year': data['year'] })

            if not fs:
                document_id = mongo.create(COLLECTION_NAME, {
                    'stock_code'     : stock_code,
                    'year'           : data['year'],
                    'total_sales'    : data['total_sales'],
                    'total_sales_yoy': data['total_sales_yoy'],
                    'business_profit': data['business_profit'],
                    'net_profit'     : data['net_profit'],
                    'eps'            : data['eps'],
                    'per'            : data['per'],
                    'pbr'            : data['pbr'],
                    'roe'            : data['roe'],
                    'evebitda'       : data['evebitda'],
                    'debt_ratio'     : data['debt_ratio'],
                    'epsroe'         : int(data['eps'] * data['roe'])
                })
                result.append(document_id)

            else:
                if '(E)' in data['year']:
                    document_id = mongo.update_one(
                        COLLECTION_NAME,
                        document_id = { 'stock_code': stock_code, 'year': data['year'] },
                        data = {
                            'total_sales'    : data['total_sales'],
                            'total_sales_yoy': data['total_sales_yoy'],
                            'business_profit': data['business_profit'],
                            'net_profit'     : data['net_profit'],
                            'eps'            : data['eps'],
                            'per'            : data['per'],
                            'pbr'            : data['pbr'],
                            'roe'            : data['roe'],
                            'evebitda'       : data['evebitda'],
                            'debt_ratio'     : data['debt_ratio'],
                            'epsroe'         : int(data['eps'] * data['roe'])
                        }
                    )
                    result.append(document_id)

    finally:
        mongo.close()

    return result
