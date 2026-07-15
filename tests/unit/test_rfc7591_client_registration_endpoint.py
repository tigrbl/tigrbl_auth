"""Endpoint tests for RFC 7591 client registration."""

import httpx
import pytest


@pytest.fixture()
async def running_app(override_get_db):
    from tigrbl_identity_server.app import app

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_legacy_client_registration_endpoint_is_removed(running_app):
    resp = await running_app.post(
        "/client/register",
        json={
            "tenant_slug": "public",
            "redirect_uris": ["https://a.example/cb"],
        },
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_rfc7591_redirect_uris_must_use_https(running_app):
    resp = await running_app.post(
        "/register",
        json={
            "tenant_slug": "public",
            "redirect_uris": ["http://insecure.example/cb"],
        },
    )
    assert resp.status_code == 400
