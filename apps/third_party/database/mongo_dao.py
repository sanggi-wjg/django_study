from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.util.exception import DBSelectNone, DBDeleteNone


class MongoDAO:

    @staticmethod
    def get_productCd_one(productCd = None):
        mongo = MongoDB()
        try:
            if not productCd: raise ValueError('Empty productCd')

            result = mongo.find_one('in_queue', { 'productCd': productCd })
            if not result: raise DBSelectNone('Non exist product')

        except Exception as e:
            raise e

        finally:
            mongo.close()

        return result

    @staticmethod
    def delete_productCd(productCd = None):
        mongo = MongoDB()
        try:
            if not productCd: raise ValueError('Empty productCd')

            document = mongo.remove('in_queue', { 'productCd': productCd })
            if document.deleted_count == 0: raise DBDeleteNone('Delete None')

        except Exception as e:
            raise e

        finally:
            mongo.close()

        return True
