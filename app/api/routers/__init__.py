"""Application API routers."""

from fastapi import APIRouter

from app.api.routers import health, metadata

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(metadata.router, tags=["metadata"])

__all__ = ["router"]
