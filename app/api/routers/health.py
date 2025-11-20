"""Health check endpoints."""

from fastapi import APIRouter

from app.schemas import health as health_schemas

router = APIRouter()


@router.get("/health", response_model=health_schemas.HealthResponse)
async def health() -> health_schemas.HealthResponse:
    """Return health check status."""
    return health_schemas.HealthResponse(status="ok")
