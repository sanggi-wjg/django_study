from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.util.exception import DBSelectNone


class MongoDAO:

    def query(self, query_type = None, **kwargs):
        try:
            if not query_type: raise Exception('query_type is empty')
            if not hasattr(self, query_type): raise Exception('query_type is not proper')

        except Exception as e:
            raise e

        mongo = MongoDB()
        try:
            dispatch_method = getattr(self, query_type)
            result = dispatch_method(mongo, **kwargs)

        except Exception as e:
            raise e

        finally:
            mongo.close()

        return result

    @staticmethod
    def get_productCd_one(mongo, productCd = None):
        try:
            if not productCd: raise ValueError('Empty productCd')

            query_result = mongo.find_one('in_queue', { 'productCd': productCd })
            if not query_result: raise DBSelectNone('Non exist product')

        except Exception as e:
            raise e

        return query_result

    @staticmethod
    def delete_productCd(mongo, productCd = None):
        try:
            if not productCd: raise ValueError('Empty productCd')

            document = mongo.remove('in_queue', { 'productCd': productCd })

        except Exception as e:
            raise e

        return document.deleted_count
