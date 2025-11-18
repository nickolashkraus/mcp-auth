"""Tests for health check endpoints."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint returns ok status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
