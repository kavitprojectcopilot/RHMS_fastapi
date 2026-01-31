from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for err in exc.errors():
        errors.append({
            "field": ".".join(map(str, err["loc"][1:])),
            "error": err["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "status": False,
            "detail": errors,
            "message": "Validation error"
        }
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "detail": exc.detail,
            "message": "Request failed"
        }
    )
