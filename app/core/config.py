"""Application settings."""

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProtectedResourceMetadataConfig(BaseModel):
    """OAuth 2.0 Protected Resource Metadata configuration."""

    resource: HttpUrl
    authorization_servers: list[str] | None = None
    scopes_supported: list[str] | None = None
    bearer_methods_supported: list[str] | None = None
    resource_signing_alg_values_supported: list[str] | None = None
    resource_name: str | None = None
    resource_documentation: HttpUrl | None = None


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    app_name: str = "MCP Authorization"
    debug: bool = False
    prefix: str = ""
    protected_resource_metadata: ProtectedResourceMetadataConfig


settings = Settings()  # type: ignore[call-arg]


def get_settings() -> Settings:
    """Get application settings."""
    return settings
