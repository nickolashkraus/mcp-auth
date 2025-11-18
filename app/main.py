"""Application entrypoint."""

from fastapi import FastAPI

from app.api.routers import router
from app.core.config import settings


def create_app() -> FastAPI:
    """Create FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.include_router(router, prefix=settings.prefix)

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {"message": "Hello, World!"}

    return app


app = create_app()
