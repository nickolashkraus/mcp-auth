"""Application API routers."""

from fastapi import APIRouter

from app.api.routers import health

router = APIRouter()

router.include_router(health.router, tags=["health"])

__all__ = ["router"]
