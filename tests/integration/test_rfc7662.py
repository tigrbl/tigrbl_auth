"""Tests for RFC 7662 token introspection compliance."""

import pytest
from httpx import AsyncClient, BasicAuth
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.orm import Client, Tenant
from tigrbl_auth.standards.oauth2.introspection import register_token, reset_tokens


async def _create_tenant_and_client(db_session: AsyncSession) -> Client:
    suffix = uuid4().hex[:8]
    tenant = Tenant(
        slug=f"introspect-{suffix}",
        name=f"Introspect {suffix}",
        email=f"introspect-{suffix}@example.com",
    )
    db_session.add(tenant)
    await db_session.commit()
    client = Client.new(
        tenant_id=tenant.id,
        client_id=str(uuid4()),
        client_secret="introspect-secret",
        redirects=["https://client.example/callback"],
    )
    db_session.add(client)
    await db_session.commit()
    return client


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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_introspect_valid_api_key(
    async_client: AsyncClient, enable_rfc7662, db_session: AsyncSession
):
    """Valid API key should yield an active introspection response."""
    client = await _create_tenant_and_client(db_session)
    register_token("active-introspection-token")
    try:
        response = await async_client.post(
            "/introspect",
            data={"token": "active-introspection-token"},
            auth=BasicAuth(str(client.id), "introspect-secret"),
        )
        assert response.status_code == 200
        body = response.json()
        assert body.get("active") is True
    finally:
        reset_tokens()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_introspect_invalid_api_key(
    async_client: AsyncClient, enable_rfc7662, db_session: AsyncSession
):
    """Invalid API key should yield inactive response per RFC 7662."""
    client = await _create_tenant_and_client(db_session)
    response = await async_client.post(
        "/introspect",
        data={"token": "does-not-exist"},
        auth=BasicAuth(str(client.id), "introspect-secret"),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("active") is False
