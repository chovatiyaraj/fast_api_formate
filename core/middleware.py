from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from token_verify import decode_access_token
from bson import ObjectId
import json

# database :
from database import users_collection    



class IPLocationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1️⃣ Client IP
        client_ip = request.client.host
        print(f"📌 Client IP: {client_ip}")

        # 2️⃣ Headers
        print("📌 Headers:", dict(request.headers))

        # 3️⃣ Query Parameters
        print("📌 Query Params:", dict(request.query_params))

        # 4️⃣ Cookies
        print("📌 Cookies:", request.cookies)

        print("📌 Path:", request.url.path)

        # 6️⃣ Body (Need to read safely)
        try:
            body_bytes = await request.body()
            if body_bytes:
                try:
                    body_data = json.loads(body_bytes.decode("utf-8"))
                except:
                    body_data = body_bytes.decode("utf-8")
                print("📌 Body:", body_data)
            else:
                print("📌 Body: Empty")
        except Exception as e:
            print("⚠️ Could not read body:", e)

        async def receive():
            return {"type": "http.request", "body": body_bytes}
        request._receive = receive

        # Continue request
        response = await call_next(request)
        return response


class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1️⃣ IP Logging
        client_ip = request.client.host
        print(f"📌 Request IP: {client_ip}")

        # 2️⃣ Token Check
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized - Missing or Invalid Token")

        token = auth_header.split(" ")[1]
        result = decode_access_token(token)
        if not result["status"]:
            raise HTTPException(status_code=401, detail=result["error"])

        payload = result["data"]
        print("✅ Token payload:", payload)

        # 3️⃣ Admin Check
        if not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="Admin access required")

        # 4️⃣ User Check in DB
        user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # 5️⃣ Store user in request.state for later use
        request.state.user = user

        # Continue request
        return await call_next(request)


