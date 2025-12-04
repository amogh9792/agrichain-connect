import time
from fastapi import Request
from app.core.logging_config import logger

async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)

    logger.info(
        f"REQUEST {request.method} {request.url.path}"
        f"status = {response.status_code} time = {duration}ms"
    )

    return response