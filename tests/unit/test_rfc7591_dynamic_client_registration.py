"""Tests for RFC 7591 dynamic client registration via HTTP server."""

import importlib

import httpx
import pytest
import pytest_asyncio

from tigrbl_auth import rfc7591
from tigrbl_identity_storage.tables.client_registration import router
from tigrbl import TigrblApp
from tigrbl_auth.tables import get_db

register_router_module = importlib.import_module("tigrbl_identity_storage.tables.client_registration")


@pytest_asyncio.fixture()
async def registration_client(db_session, monkeypatch):
    app = TigrblApp()
    app.include_router(router)
    app.router.dependency_overrides[get_db] = lambda: db_session
    monkeypatch.setattr(register_router_module, "_sync_client_registration", lambda *args, **kwargs: None)
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="https://test") as client:
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
    assert resp.status_code == 200
    assert resp.json()["client_id"]
