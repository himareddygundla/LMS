from .mongo import get_mongo_db


def get_logs_db():
    return get_mongo_db()
