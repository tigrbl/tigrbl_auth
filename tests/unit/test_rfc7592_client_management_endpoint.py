"""Endpoint availability tests for RFC 7592 client management."""

import httpx
import pytest


@pytest.fixture()
async def running_app(override_get_db):
    from tigrbl_auth_backend_app_public import app

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_client_management_unknown_client_returns_404(running_app):
    resp = await running_app.patch(
        "/client/ffffffff-ffff-ffff-ffff-ffffffffffff",
        json={"redirect_uris": ["https://b.example/cb"]},
    )
    assert resp.status_code == 404
