from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging_config import logger


# ---------------------------------------------------
# Handle FastAPI / Pydantic Validation Errors (422)
# ---------------------------------------------------
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        f"VALIDATION ERROR at {request.method} {request.url}: {exc.errors()}"
    )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# ---------------------------------------------------
# Handle HTTPException (400, 401, 403, 404, etc.)
# ---------------------------------------------------
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(
        f"HTTP ERROR at {request.method} {request.url}: "
        f"status={exc.status_code}, detail={exc.detail}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# ---------------------------------------------------
# Handle ALL other unhandled Python exceptions (500)
# ---------------------------------------------------
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"UNHANDLED SERVER ERROR at {request.method} {request.url}: {str(exc)}",
        exc_info=True  # logs full traceback
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
