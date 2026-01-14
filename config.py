
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27019  
MONGO_DB = "arbres"
MONGO_COLLECTION = "arbres"

# co
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

def get_client():
    return MongoClient(MONGO_URI)

def get_db():
    client = get_client()
    return client[MONGO_DB]

def get_collection():
    db = get_db()
    return db[MONGO_COLLECTION]

