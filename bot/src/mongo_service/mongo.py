from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class MongoDB:
    def __init__(self, uri, database_name, collection_name):
        self.client = MongoClient(uri, server_api=ServerApi("1"))
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.document = {}

    def add_data(self, key, data):
        self.document[key] = data

    def commit_data(self):
        if self.document:
            self.collection.insert_one(self.document)
            print("Data committed to MongoDB.")
            self.document = {}
        else:
            print("No data to commit.")
