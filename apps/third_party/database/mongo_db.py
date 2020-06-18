import pymongo


class MongoDB:
    _instance = None
    client = pymongo.MongoClient(host = '172.17.0.3', port = 27017, username = 'root', password = 'wpdlwl')
    db = client.backend
    """
    :type client: pymongo.MongoClient
    :type db: pymongo.MongoClient.Collections
    """

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)

        return cls._instance

    def __del__(self):
        self.close()

    """
    INSERT
    
    :rtype InsertOneResult, InsertManyResult
    :returns properties
        inserted_id
        deleted_count
    """

    def create(self, collection_name: str, data):
        document = self.db[collection_name].insert_one(data)
        return document.inserted_id

    def create_bulk(self, collection_name: str, data):
        document = self.db[collection_name].insert_many(data)
        return document.inserted_ids

    """
    SELECT
    """

    def find_one(self, collection_name: str, query, limit = None, sort = None, projection = None):
        if projection is None:
            projection = { '_id': False }

        return self.db[collection_name].find_one(query, projection = projection)

    def find_list(self, collection_name: str, query, limit = None, sort = None, projection = None):
        if projection is None:
            projection = { '_id': False }

        return self.db[collection_name].find(query, projection = projection)

    def count(self, collection_name: str, query):
        return self.db[collection_name].count_documents(query)

    """
    UPDATE
    
    :rtype UpdateResult
    :returns properties
        raw_result : {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
        matched_count
        modified_count
        upserted_id
    """

    def update_one(self, collection_name: str, document_id, data, upsert = False):
        document = self.db[collection_name].update_one(document_id, { '$set': data }, upsert = upsert)
        return document

    def update_list(self, collection_name: str, document_id, data, upsert = False):
        document = self.db(collection_name).update_many(document_id, { '$set': data }, upsert = upsert)
        return document

    """
    DELETE
    
    :rtype DeleteResult
    :returns properties
        raw_result
        deleted_count
    """

    def delete_one(self, collection_name: str, document_id):
        document = self.db[collection_name].delete_one(document_id)
        return document

    def delete_list(self, collection_name: str, document_id):
        document = self.db[collection_name].delete_many(document_id)
        return document

    """
    ETC
    """

    def close(self):
        self.client.close()

    def get_databases(self):
        return self.client.list_database_names()

    def get_collections(self):
        return self.db.list_collection_names()
