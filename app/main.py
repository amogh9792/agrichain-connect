from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.user_router import router as user_router
from app.api.routes.auth_router import router as auth_router 
from app.api.routes.farmer_router import router as farmer_router

app = FastAPI(title="Agrichain Connect")

app.include_router(health_router, prefix="/api")
app.include_router(user_router)
app.include_router(auth_router, prefix="/auth")  
app.include_router(farmer_router)