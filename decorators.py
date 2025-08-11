# app/auth/decorators.py
from functools import wraps
from fastapi import Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import jwt
from bson import ObjectId
from core.config import SECRET_KEY, ALGORITHM
from database import users_collection
from core.responses import error_response
from token_verify import decode_access_token


def user_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                return JSONResponse(content=error_response("Unauthorized"), status_code=401)
            token = token.split(" ")[1]
            try:
                # 🔐 Decode token using shared function
                result = decode_access_token(token)
                if not result["status"]:
                    return JSONResponse(content=error_response(result["error"]), status_code=401)
                payload = result["data"]    
                print("Admin Require Token check payload is ====>", payload)
                
                user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})
                if not user:
                    return JSONResponse(content=error_response("User not found"), status_code=401)
                request.state.user = user
                return await func(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return JSONResponse(content=error_response("Token expired"), status_code=401)
            except Exception as e :
                return JSONResponse(content=error_response("Invalid token"), status_code=401)
        return wrapper
    return decorator


# def admin_required():
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(request: Request, *args, **kwargs):
#             token = request.headers.get("Authorization")
#             if not token or not token.startswith("Bearer "):
#                 return JSONResponse(content=error_response("Unauthorized"), status_code=401)
#             token = token.split(" ")[1]
#             print("----------------------------------------- Token ==>", token, type(token))
#             try:
#                 payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#                 print("PayLoad is ====>", payload)
#                 if not payload.get("is_admin"):
#                     return JSONResponse(content=error_response("Admin access required"), status_code=403)
#                 user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})
#                 if not user:
#                     return JSONResponse(content=error_response("User not found"), status_code=401)
#                 request.state.user = user
#                 return await func(request, *args, **kwargs)
#             except Exception:
#                 return JSONResponse(content=error_response("Invalid token"), status_code=401)
#         return wrapper
#     return decorator



# ✅ Dependency Function
async def admin_required(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = token.split(" ")[1]
    # try:
    # Use decode function
    result = decode_access_token(token)
    
    if not result["status"]:
        raise HTTPException(status_code=401, detail=result["error"])
    
    payload = result["data"]
    
    print("Admin Require Token check payload is ====>", payload)
    
    if not payload.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")

    user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    request.state.user = user
    return user  # ✅ Return user if you want to use in route
    # except Exception as e:
    #     print("-------------------------------------->", e)
    #     raise HTTPException(status_code=401, detail="Invalid token")




