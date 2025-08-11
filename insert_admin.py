# insert_admin.py

from pymongo import MongoClient
from token_verify import hash_password

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["oceanmtech_fast_api"]
users_collection = db["users"]

# Admin User Data
admin_user = {
    "username": "admin",
    "email": "admin@ocean.com",
    "password": hash_password("admin123"),  # Hash the password
    "is_admin": True,
    "is_user": False
}

# Check if already exists
if users_collection.find_one({"email": admin_user["email"]}):
    print("Admin already exists.")
else:
    users_collection.insert_one(admin_user)
    print("✅ Admin user inserted.")
