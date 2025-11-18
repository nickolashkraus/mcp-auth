"""Tests for metadata endpoints."""

from fastapi.testclient import TestClient


def test_protected_resource_metadata(client: TestClient):
    """Test protected resource metadata endpoint returns expected data."""
    response = client.get("/.well-known/oauth-protected-resource")
    assert response.status_code == 200
    assert response.json() == {
        "resource": "https://localhost:8000/",
        "authorization_servers": ["https://localhost:8000"],
        "scopes_supported": ["read:data", "write:data"],
        "bearer_methods_supported": ["header"],
        "resource_signing_alg_values_supported": ["RS256"],
        "resource_name": "MCP Authorization",
        "resource_documentation": "https://localhost:8000/docs",
    }
