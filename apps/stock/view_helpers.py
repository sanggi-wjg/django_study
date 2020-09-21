import pymongo

from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.util.colorful import print_yellow


def stock_detail_get_context(stock_code: str) -> dict:
    def _get_sums(data: dict):
        foreign_sum, company_sum = 0, 0

        for d in data:
            foreign_sum += d.get('foreign_purchase_volume')
            company_sum += d.get('company_purchase_volume')

        return foreign_sum, company_sum

    mongo = MongoDB()
    try:
        finance_info = mongo.find_list('finance_info', { "stock_code": stock_code }).sort('year')
        demand_info = mongo.find_list('demand_info', { "stock_code": stock_code }).sort('date', pymongo.DESCENDING)
        summary_demand_info = {
            _get_sums(mongo.find_list('demand_info', { "stock_code": stock_code }).sort('date', pymongo.DESCENDING).limit(5)),
            _get_sums(mongo.find_list('demand_info', { "stock_code": stock_code }).sort('date', pymongo.DESCENDING).limit(10)),
            _get_sums(mongo.find_list('demand_info', { "stock_code": stock_code }).sort('date', pymongo.DESCENDING).limit(20)),
            _get_sums(mongo.find_list('demand_info', { "stock_code": stock_code }).sort('date', pymongo.DESCENDING).limit(30)),
        }
    finally:
        mongo.close()

    return {
        'finance_info'       : finance_info,
        'demand_info'        : demand_info,
        'summary_demand_info': summary_demand_info,
    }
