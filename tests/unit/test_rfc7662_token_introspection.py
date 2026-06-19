"""Tests for OAuth2 token introspection compliance with RFC 7662."""

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_identity_server.framework import TigrblApp, status
from tigrbl_identity_storage.tables import _oauth_introspection as introspection_module
from tigrbl_identity_storage.tables._oauth_introspection import (
    register_token_async,
    reset_tokens_async,
    router,
)


# RFC 7662 specification excerpt for reference within tests
RFC7662_SPEC = """
RFC 7662 - OAuth 2.0 Token Introspection

2.1. Introspection Request
   The introspection endpoint MUST handle HTTP POST requests with
   Content-Type application/x-www-form-urlencoded.  The body MUST
   include the "token" parameter.

2.2. Introspection Response
   The introspection endpoint responds with a JSON object that includes
   an "active" boolean value.  If the token is invalid, expired, revoked,
   or otherwise not active, the value of "active" MUST be false.
"""


@pytest.mark.unit
@pytest.mark.asyncio
async def test_introspection_endpoint_returns_active_field(enable_rfc7662):
    """RFC 7662 §2.2: Response must include an 'active' boolean."""
    app = TigrblApp()
    app.include_router(router)
    await register_token_async("dummy")

    async def _allow(*_args, **_kwargs):
        return None

    transport = ASGITransport(app=app)
    original = introspection_module._authorize_introspection_caller
    try:
        introspection_module._authorize_introspection_caller = _allow
        async with AsyncClient(transport=transport, base_url="https://test") as client:
            resp = await client.post("/introspect", data={"token": "dummy"})
        assert resp.status_code == status.HTTP_200_OK
        body = resp.json()
        assert body.get("active") is True
    finally:
        introspection_module._authorize_introspection_caller = original
        await reset_tokens_async()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_introspection_requires_token_parameter(enable_rfc7662):
    """RFC 7662 §2.1: Request body MUST include the 'token' parameter."""
    app = TigrblApp()
    app.include_router(router)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as client:
        resp = await client.post("/introspect", data={})
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.unit
@pytest.mark.asyncio
async def test_introspection_requires_authenticated_caller(enable_rfc7662):
    app = TigrblApp()
    app.include_router(router)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as client:
        resp = await client.post("/introspect", data={"token": "dummy"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
