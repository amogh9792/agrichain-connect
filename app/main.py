from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.user_router import router as user_router

app = FastAPI(title="Agrichain Connect")

app.include_router(health_router, prefix="/api")
app.include_router(user_router)