from fastapi.responses import JSONResponse


def success(data=None, message="ok", status_code=200):
    """Return a standardized success response as JSON"""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )


def error(code: str, message: str, fields=None, status_code=400):
    """Return a standardized error response as JSON"""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "fields": fields,
            },
        },
    )

