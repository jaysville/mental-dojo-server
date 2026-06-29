from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success(data=None, message="ok", status_code=200):
    """Standard success response"""
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({
            "success": True,
            "message": message,
            "data": data,
        }),
    )

def error(code: str, message: str, fields=None, status_code=400):
    """Standard error response"""
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "fields": fields,
            },
        }),
    )