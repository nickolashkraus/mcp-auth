"""Application entrypoint."""

from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.types import ASGIApp

from app.api.routers import router
from app.core.config import settings
from app.schemas import mcp as mcp_schemas
from app.schemas import root as root_schemas


def create_app(mcp_app: ASGIApp) -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=mcp_app.lifespan,
    )

    app.include_router(router, prefix=settings.prefix)

    @app.get("/", response_model=root_schemas.RootResponse)
    async def root() -> root_schemas.RootResponse:
        """Root endpoint."""
        return root_schemas.RootResponse(message="Hello, World!")

    # Mount the MCP server.
    app.mount("/mcp", mcp_app)

    return app


def create_mcp_app() -> ASGIApp:
    """Create FastMCP application."""
    mcp = FastMCP(
        name=settings.mcp_app_name,
    )

    @mcp.tool
    async def hello() -> mcp_schemas.ToolResponse:
        """Return 'Hello, World!'"""
        return mcp_schemas.ToolResponse(message="Hello, World!")

    # Create ASGI app from MCP server.
    mcp_app = mcp.http_app(path="/")

    return mcp_app


mcp_app = create_mcp_app()
app = create_app(mcp_app=mcp_app)
