import json
from datetime import datetime

from apps.in_queue.vos import InQueue
from apps.third_party.database.mongo_dao import MongoDAO
from apps.third_party.util.exception import DBSelectNone


class Mongo_InQueue(MongoDAO):

    @staticmethod
    def get_list(mongo):
        try:
            query_result = mongo.find_list('in_queue', { })

        except Exception as e:
            raise e

        return query_result

    @staticmethod
    def get_in_queue_productCd_one(mongo, productCd = None):
        try:
            if not productCd: raise ValueError('Empty productCd')

            query_result = mongo.find_one('in_queue', { 'productCd': productCd })
            if not query_result: raise DBSelectNone('Non exist product')

        except Exception as e:
            raise e

        return query_result

    @staticmethod
    def insert_list(mongo, data):
        if not data: raise ValueError('Empty data')

        queues = _setup_in_queue(data)
        document_ids = mongo.create_bulk('in_queue', [q.__dict__ for q in queues])

        return document_ids

    @staticmethod
    def delete_productCd(mongo, productCd = None):
        try:
            if not productCd: raise ValueError('Empty productCd')

            document = mongo.remove('in_queue', { 'productCd': productCd })

        except Exception as e:
            raise e

        return document.deleted_count


def _setup_in_queue(data):
    datalist = json.loads(data).get('datalist')
    queues = []

    for data in datalist:
        queue = InQueue()
        queue.packageCd = data.get('packageCd')
        queue.productCd = data.get('productCd')
        queue.productItemCd = data.get('productItemCd')
        queue.productName = data.get('productName')
        queue.productUnitPrice = float(data.get('productUnitPrice'))
        queue.inOrderCd = data.get('inOrderCd')
        queue.inOrderDate = datetime.strptime(data.get('inOrderDate'), '%Y-%m-%d %H:%M:%S')

        queues.append(queue)

    return queues
