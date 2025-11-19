"""Application entrypoint."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

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
    async def root() -> JSONResponse:
        """Root endpoint."""
        return JSONResponse(content={"message": "Hello, World!"})

    return app


app = create_app()
