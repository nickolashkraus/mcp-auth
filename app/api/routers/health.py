"""Health endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """Health endpoint."""
    return {"status": "ok"}
