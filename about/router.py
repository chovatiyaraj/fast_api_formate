from fastapi import APIRouter, Request, Depends, UploadFile, File, BackgroundTasks, Form
from typing import List
from decorators import admin_required, user_required
from core.responses import success_response, error_response
import os
import uuid
import time

router = APIRouter(prefix="/about", tags=["About"])

# Create static/uploads folder if not exist
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



# ✅ Background function
def count_numbers(n: int):
    for i in range(1, n + 1):
        print(f"Background: {i}")
        time.sleep(1)  # 1 second delay

# ✅ API endpoint
@router.post("/start-task")
async def start_background_task(number: int, background_tasks: BackgroundTasks):
    print("========================================================================")
    background_tasks.add_task(count_numbers, number)
    return success_response("All files uploaded successfully!", number)



def notify_user(email: str, message: str):
    print(f"Sending email to {email}: {message}")
    time.sleep(3)
    print("Email sent.")

@router.post("/notify")
async def notify(background_tasks: BackgroundTasks, email: str = Form(...)):
    background_tasks.add_task(notify_user, email, "Your request is completed.")
    return {"message": "Email sending started in background."}





# ✅ File upload API
@router.post("/upload")
async def upload_file(files:List[UploadFile] = File(...)):
    allowed_extensions = ["jpg", "jpeg", "png", "gif", "mp4", "avi", "mov", "mkv",'webm']
    uploaded_files = []

    for file in files:
        file_ext = file.filename.split(".")[-1].lower()

        if file_ext not in allowed_extensions:
            return error_response(f"Unsupported file type: .{file_ext}", 400)

        # Generate unique name and save file
        unique_name = f"{uuid.uuid4()}.{file_ext}"
        save_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())

        file_url = f"/static/uploads/{unique_name}"
        uploaded_files.append(file_url)

    return success_response("All files uploaded successfully!", uploaded_files)



@router.get("/")
async def about_info():
    return success_response("About API accessed successfully.", "Welcome to the About section!")

@router.get("/user/data")
@user_required()
async def user_data(request: Request):
    user = request.state.user  # ✅ Access user from decorator
    print("======================= User Data Get Route Call ====================",user)
    return success_response(
        f"Welcome {user['username']}",
        {
            "role": "user",
            "username": user["username"],
            "email": user["email"]
        }
    )



@router.get("/admin/data")
# @admin_required()
async def admin_data(request: Request, user: dict = Depends(admin_required)):
    print("Request is ==>", request)
    print("🔹 IP Address:", request.client.host)
    print("🔹 Port:", request.client.port)
    print("🔹 Method:", request.method)
    print("🔹 Full URL:", request.url)
    print("🔹 Headers:", request.headers)
    print("🔹 Cookies:", request.cookies)
    
    # user = request.state.user
    return success_response(
        f"Welcome {user['username']} (Admin)",
        {
            "role": "admin",
            "username": user["username"],
            "email": user["email"]
        }
    )