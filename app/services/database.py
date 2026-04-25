import certifi
from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
from app.config import get_mongo_uri, get_db_name

_client: Optional[MongoClient] = None
_db: Optional[Database] = None


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(get_mongo_uri(), tlsCAFile=certifi.where())
    return _client


def get_database() -> Database:
    global _db
    if _db is None:
        client = get_mongo_client()
        _db = client[get_db_name()]
    return _db


def get_sesiones_collection():
    db = get_database()
    return db["sesiones"]


def get_operaciones_collection():
    db = get_database()
    return db["operaciones"]


def close_connection():
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None