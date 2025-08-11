# app/main.py
from fastapi import FastAPI, Request, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.openapi.utils import get_openapi
from authentication.routes import router as auth_router
from about.router import router as about_router
from decorators import user_required, admin_required
import time
from core.middleware import *

app = FastAPI(
    title="Secure API",
    description="Login/Register API with Role-based Access",
    version="1.0.0",
    docs_url=None
)
# Add IP logging middleware
app.add_middleware(IPLocationMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("about Route Middleware is ====>", request, call_next)
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print("Response is ====>", response)
    return response



# app = FastAPI(
#     title="Secure API",
#     description="Login/Register API with Role-based Access",
#     version="1.0.0",
#     docs_url=None,
#     redoc_url=None,
#     openapi_url=None
# )


# Protected Swagger /docs route
# @app.get("/docs", include_in_schema=False)
# # @user_required()
# # @admin_required()
# # async def custom_docs(request: Request, user: dict = Depends(admin_required)):
# async def custom_docs(request: Request):
#     print("User is ==>")
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure Docs")

# Register Auth Routes
app.include_router(auth_router)
app.include_router(about_router)

# Custom 404 Not Found
@app.exception_handler(StarletteHTTPException)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "success": False,
                "message": "Route not found.",
                "data": ""
            }
        )
    elif exc.status_code == 403:
        return JSONResponse(
            status_code=403,
            content={
                "status": 403,
                "success": False,
                "message": "Access forbidden.",
                "data": ""
            }
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "success": False,
                "message": str(exc.detail),
                "data": ""
            }
        )

# ✅ Custom 400 Bad Request
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("================================================ 400  =============================================================")
    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "success": False,
            "message": "Bad Request - Validation Error",
            "data": exc.errors()
        }
    )

# ✅ Custom 500 Internal Server Error Handler
@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception):
    print("500 ==========================>", exc)
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "success": False,
            "message": "Internal Server Error",
            "data": str(exc)
        }
    )

# ✅ Run FastAPI app with uvicorn
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("app:app", host="0.0.0.0", port=2000, reload=True)
    uvicorn.run("app:app", host="0.0.0.0", port=2000)
    # uvicorn.run("app:app", host="0.0.0.0", port=2000)
