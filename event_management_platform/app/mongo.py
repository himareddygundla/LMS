import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://mongo:27017')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'event_platform')

_client = None
_database = None


def get_mongo_db():
    global _client, _database
    if _database is None:
        _client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)
        _database = _client[MONGO_DB_NAME]
    return _database


def safe_log(collection: str, payload: dict):
    try:
        db = get_mongo_db()
        payload['created_at'] = datetime.utcnow()
        db[collection].insert_one(payload)
    except PyMongoError:
        # Avoid breaking the primary SQL workflow if logging fails.
        pass


def count_documents(collection: str) -> int:
    try:
        db = get_mongo_db()
        return db[collection].count_documents({})
    except PyMongoError:
        return 0
