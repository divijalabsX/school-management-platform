from fastapi import APIRouter

from app.routes import health, auth, organisation


api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(organisation.router)