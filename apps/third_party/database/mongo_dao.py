from apps.third_party.database.mongo_db import MongoDB


class MongoDAO:

    def query(self, query_type = None, **kwargs):
        try:
            if not query_type: raise Exception('query_type is empty')
            if not hasattr(self, query_type): raise Exception('query_type is not declared')

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
