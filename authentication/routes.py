# app/auth/routes.py
from fastapi import APIRouter, Request, status
from database import users_collection
from core.responses import success_response, error_response
from token_verify import hash_password, verify_password, create_access_token
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)



@router.post("/register")
# async def register(request: Request):
async def register_user(user: RegisterUser):
    if user.password != user.confirm_password:
        return error_response("Passwords do not match", status=status.HTTP_400_BAD_REQUEST)

    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        return error_response("Email already registered", status=status.HTTP_409_CONFLICT)

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "is_admin": False,
        "is_user": True
    }

    users_collection.insert_one(user_data)
    return success_response("User registered successfully", status=status.HTTP_201_CREATED)

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if not user:
        return error_response("User not found", status=404)

    if not verify_password(password, user["password"]):
        return error_response("Invalid password", status=401)

    token = create_access_token(user)
    print("Login Token is ===>", token)
    return success_response("Login successful", {"token": token})

