from sys import exit as exiter

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from Mikobot import DB_NAME, LOGGER, MONGO_DB_URI

from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://demonxyonko:<db_password>@rickycyan.fswqzgl.mongodb.net/?retryWrites=true&w=majority&appName=rickycyan"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["your-db-name"]

try:
    Mikobot_db_client = MongoClient(MONGO_DB_URI)
except PyMongoError as f:
    LOGGER.error(f"Error in Mongodb: {f}")
    exiter(1)
Mikobot_main_db = Mikobot_db_client[DB_NAME]


class MongoDB:
    """Class for interacting with Bot database."""

    def __init__(self, collection) -> None:
        self.collection = Mikobot_main_db[collection]

    # Insert one entry into collection
    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    # Find one entry from collection
    def find_one(self, query):
        result = self.collection.find_one(query)
        if result:
            return result
        return False

    # Find entries from collection
    def find_all(self, query=None):
        if query is None:
            query = {}
        return list(self.collection.find(query))

    # Count entries from collection
    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    # Delete entry/entries from collection
    def delete_one(self, query):
        self.collection.delete_many(query)
        return self.collection.count_documents({})

    # Replace one entry in collection
    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    # Update one entry from collection
    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def close():
        return Mikobot_db_client.close()


def __connect_first():
    _ = MongoDB("test")
    LOGGER.info("Initialized Mongo Database!\n")


__connect_first()
