# app/database.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["oceanmtech_fast_api"]

print("Database is ==>", db)
users_collection = db["users"]
