"""Root endpoint response models."""

from pydantic import BaseModel


class RootResponse(BaseModel):
    """Response model for the root endpoint."""

    message: str
