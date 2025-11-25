"""Tests for metadata endpoints."""

from fastapi.testclient import TestClient

from app.core.config import settings


def test_protected_resource_metadata(client: TestClient) -> None:
    """Test protected resource metadata endpoint returns expected data."""
    response = client.get("/.well-known/oauth-protected-resource")
    assert response.status_code == 200
    assert response.json() == {
        "resource": str(settings.protected_resource_metadata.resource),
        "authorization_servers": settings.protected_resource_metadata.authorization_servers,
        "scopes_supported": settings.protected_resource_metadata.scopes_supported,
        "bearer_methods_supported": settings.protected_resource_metadata.bearer_methods_supported,
        "resource_signing_alg_values_supported": settings.protected_resource_metadata.resource_signing_alg_values_supported,
        "resource_name": settings.protected_resource_metadata.resource_name,
        "resource_documentation": str(
            settings.protected_resource_metadata.resource_documentation
        ),
    }
