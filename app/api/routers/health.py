"""Health check endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health() -> JSONResponse:
    """Return health check status."""
    return JSONResponse(content={"status": "ok"})
