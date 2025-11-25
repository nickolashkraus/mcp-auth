"""MCP tool endpoint response model."""

from pydantic import BaseModel


class ToolResponse(BaseModel):
    """Response model for the MCP tool endpoint."""

    message: str
