from fastapi.responses import JSONResponse


# app/core/responses.py
def success_response(message, data="", status=200):
    return JSONResponse(
        status_code=status,
        content={
            "status": status,
            "success": True,
            "message": message,
            "data": data
        }
    )

def error_response(message, data="", status=400):
    return JSONResponse(
        status_code=status,
        content={
            "status": status,
            "success": False,
            "message": message,
            "data": data
        }
    )