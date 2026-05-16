from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "globaldata_db")

def get_db():
    client = MongoClient(
        "mongodb+srv://praveen:Praveen%407995@cluster0.q9jmz6k.mongodb.net/",
        serverSelectionTimeoutMS=60000,
        connectTimeoutMS=60000,
        socketTimeoutMS=60000,
        tlsCAFile=certifi.where()
    )
    return client[DB_NAME]

def get_col(name):
    return get_db()[name]

if __name__ == "__main__":
    try:
        db = get_db()
        db.command("ping")
        print(f"[OK] Connected to MongoDB | Database: {db.name}")
    except Exception as e:
        print(f"[ERROR] {e}")