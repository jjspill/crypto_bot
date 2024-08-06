from datetime import datetime

from pytz import timezone


class MongoDB:
    def __init__(self, client, database_name, collection_name):
        self.client = client
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.collection.create_index(
            [("timestamp", 1)]
        )  # Ensure indexing on the timestamp
        self.document = {}

    def add_data(self, data: dict):
        self.document.update(data)

    def commit_data(self):
        if self.document:
            est = timezone("US/Eastern")
            current_time_est = (
                datetime.utcnow().replace(tzinfo=timezone("UTC")).astimezone(est)
            )
            # This should run on the hour so we can aggregate data by the hour
            formatted_time = current_time_est.strftime("%Y-%m-%d %H:00")
            self.document["timestamp"] = formatted_time
            print("Data to commit:", self.document)
            result = self.collection.insert_one(self.document)
            print("Data inserted with ID:", result.inserted_id)
            print(
                "Data committed to MongoDB with timestamp:", self.document["timestamp"]
            )
            self.document = {}
        else:
            print("No data to commit.")
