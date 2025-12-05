from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.user_router import router as user_router
from app.api.routes.auth_router import router as auth_router 
from app.api.routes.farmer_router import router as farmer_router
from app.api.routes.vendor_router import router as vendor_router
from app.api.routes.produce_router import router as produce_router
from app.api.routes.market_router import router as market_router


from app.middleware.request_logger import log_requests
from app.core.logging_config import logger
from app.middleware.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    global_exception_handler,)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Agrichain Connect")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

logger.info("FastAPI application started")

app.include_router(health_router, prefix="/api")
app.include_router(user_router)
app.include_router(auth_router, prefix="/auth")  
app.include_router(farmer_router)
app.include_router(vendor_router)
app.include_router(produce_router)
app.include_router(market_router)