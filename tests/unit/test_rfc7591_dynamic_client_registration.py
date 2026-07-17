"""Tests for RFC 7591 dynamic client registration via HTTP server."""

import httpx
import pytest
import pytest_asyncio
from types import SimpleNamespace

from tigrbl_auth import rfc7591
from tigrbl_auth_backend_app_core.surfaces.client_registration_surface import router
from tigrbl import TigrblApp
from tigrbl_identity_storage_runtime.engine import get_db
import tigrbl_auth_backend_app_core.surfaces.client_registration_surface as registration_surface


@pytest_asyncio.fixture()
async def registration_client(db_session, monkeypatch):
    deployment = SimpleNamespace(
        issuer="https://test",
        profile="production",
        flags={"require_tls": True},
        flag_enabled=lambda name: name in {"enable_rfc7591", "enable_rfc7592"},
    )
    monkeypatch.setattr(registration_surface, "_deployment", lambda request: deployment)
    app = TigrblApp()
    app.include_router(router)
    app.router.dependency_overrides[get_db] = lambda: db_session
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="https://test"
    ) as client:
        yield client


def test_rfc7591_spec_url() -> None:
    """Module exports the specification URL."""
    assert rfc7591.RFC7591_SPEC_URL.endswith("7591")


@pytest.mark.asyncio
async def test_register_client_via_server(registration_client):
    """Client can register through the running server."""
    resp = await registration_client.post(
        "/register",
        json={
            "tenant_slug": "public",
            "redirect_uris": ["https://a.example/cb"],
        },
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["client_id"]


@pytest.mark.asyncio
async def test_registration_management_lifecycle_via_http_carrier(
    registration_client,
):
    created_response = await registration_client.post(
        "/register",
        json={
            "tenant_slug": "public",
            "redirect_uris": ["https://a.example/cb"],
            "client_name": "Original",
        },
    )
    assert created_response.status_code == 200, created_response.text
    created = created_response.json()
    client_id = created["client_id"]
    token = created["registration_access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    fetched = await registration_client.get(
        f"/register/{client_id}",
        headers=headers,
    )
    assert fetched.status_code == 200, fetched.text
    assert fetched.json()["client_name"] == "Original"
    assert "client_secret" not in fetched.json()

    updated = await registration_client.put(
        f"/register/{client_id}",
        headers=headers,
        json={
            "client_name": "Changed",
            "redirect_uris": ["https://b.example/cb"],
        },
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["client_name"] == "Changed"
    assert updated.json()["redirect_uris"] == ["https://b.example/cb"]

    invalid = await registration_client.get(
        f"/register/{client_id}",
        headers={"Authorization": "Bearer invalid"},
    )
    assert invalid.status_code == 401

    deleted = await registration_client.delete(
        f"/register/{client_id}",
        headers=headers,
    )
    assert deleted.status_code == 200, deleted.text
    assert deleted.json() == {"status": "deleted", "client_id": client_id}

    after_delete = await registration_client.get(
        f"/register/{client_id}",
        headers=headers,
    )
    assert after_delete.status_code == 404
