import pymongo
from bson import ObjectId


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

    ##############################################################################################
    # INSERT
    ##############################################################################################
    def create(self, collection_name: str, data):
        document = self.db[collection_name].insert_one(data)
        return document.inserted_id

    def create_bulk(self, collection_name: str, data):
        document = self.db[collection_name].insert_many(data)
        return document.inserted_ids

    ##############################################################################################
    # SELECT
    ##############################################################################################
    def find_one(self, collection_name: str, query):
        return self.db[collection_name].find_one(query)

    def find_list(self, collection_name: str, query):
        return self.db[collection_name].find(query)

    def count(self, collection_name: str, query):
        return self.db[collection_name].count_documents(query)

    ##############################################################################################
    # UPDATE
    ##############################################################################################
    def update(self, collection_name: str, document_id, data, multi = True):
        document = self.db(collection_name).update(document_id, { "$set": data }, multi = multi)
        return document.acknowledged

    def update_or_create(self, collection_name: str, document_id, data):
        document = self.db[collection_name].update_one(document_id, { "$set": data }, upsert = True)
        return document.acknowledged

    ##############################################################################################
    # DELETE
    ##############################################################################################
    def remove(self, collection_name: str, document_id):
        document = self.db[collection_name].delete_one(document_id)
        return document.acknowledged

    ##############################################################################################
    # ETC
    ##############################################################################################
    def close(self):
        self.client.close()

    def get_databases(self):
        return self.client.list_database_names()

    def get_collections(self):
        return self.db.list_collection_names()
