"""Application entrypoint."""

from fastapi import FastAPI

from app.api.routers import router
from app.core.config import settings
from app.schemas import root as root_schemas


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.include_router(router, prefix=settings.prefix)

    @app.get("/", response_model=root_schemas.RootResponse)
    async def root() -> root_schemas.RootResponse:
        """Root endpoint."""
        return root_schemas.RootResponse(message="Hello, World!")

    return app


app = create_app()
