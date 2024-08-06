import os
from datetime import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pytz import timezone

CLIENT = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi("1"))


class MongoDB:
    def __init__(self, database_name, collection_name):
        self.client = CLIENT
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.collection.create_index(
            [("timestamp", 1)]
        )  # Ensure indexing on the timestamp
        self.document = {}

    def add_data(self, key, data):
        self.document[key] = data

    def commit_data(self):
        if self.document:
            est = timezone("US/Eastern")
            current_time_est = (
                datetime.utcnow().replace(tzinfo=timezone("UTC")).astimezone(est)
            )
            formatted_time = current_time_est.strftime("%Y-%m-%d %H:00")
            self.document["timestamp"] = formatted_time
            self.collection.insert_one(self.document)
            print(
                "Data committed to MongoDB with timestamp:", self.document["timestamp"]
            )
            self.document = {}
        else:
            print("No data to commit.")
