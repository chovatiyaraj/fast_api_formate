# app/auth/utils.py
from datetime import datetime, timedelta
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from jose import ExpiredSignatureError, JWTError
from passlib.context import CryptContext
import time
from cryptography.fernet import Fernet
from core.config import *

# fernate_key = b'MkAlXecFzVFn_iOPQ35dO6Xr-sUZvN1Q7W8-TzrgLM4='
f = Fernet(fernate_key)

# 🔁 Encode function
def encode_string_data(data):
    start = time.time()
    encrypted = f.encrypt(str(data).encode())
    end = time.time()
    print(f"Encode Execution Time: {(end - start)*1000:.3f} ms")
    return encrypted

# 🔁 Decode function
def decode_string_data(encrypted_data):
    start = time.time()
    decrypted = f.decrypt(encrypted_data).decode()
    end = time.time()
    print(f"Decode Execution Time: {(end - start)*1000:.3f} ms")
    return decrypted


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(user: dict):
    expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    print("access Token is ===>", expire)
    payload = {
        "user_id": str(user["_id"]),
        "is_admin": user.get("is_admin", False),
        "is_user": user.get("is_user", True),
        "exp": expire,
        "iat": int(time.time()),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



def decode_access_token(token: str):
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "status": True,
            "data": payload
        }
    except ExpiredSignatureError:
        return {
            "status": False,
            "error": "Token has expired"
        }
    except JWTError as e:
        return {
            "status": False,
            "error": "Invalid token",
            "details": str(e)
        }
        
