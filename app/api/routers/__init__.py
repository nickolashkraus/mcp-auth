"""Application API routers."""

from fastapi import APIRouter

from app.api.routers import health, metadata

router = APIRouter()

router.include_router(health.router)
router.include_router(metadata.router)

__all__ = ["router"]
