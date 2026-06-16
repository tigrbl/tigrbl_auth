"""Tests for OAuth 2.0 Token Revocation compliance with RFC 7009."""

import pytest
from http import HTTPStatus as status
from httpx import AsyncClient

from tigrbl_auth.runtime_cfg import settings
from tigrbl_auth.rfc.rfc7009 import is_revoked_async, reset_revocations_async

# RFC 7009 specification excerpt for reference within tests
RFC7009_SPEC = """
RFC 7009 - OAuth 2.0 Token Revocation

2.2. Revocation Response
   The authorization server responds with HTTP status code 200
   in all cases, even if the token is invalid.
"""


@pytest.mark.unit
@pytest.mark.asyncio
async def test_revoke_returns_200_and_marks_token_revoked(
    enable_rfc7009, async_client: AsyncClient
):
    """RFC 7009 §2.2: Revocation returns HTTP 200 and token becomes invalid."""
    resp = await async_client.post("/revoke", data={"token": "abc"})
    assert resp.status_code == status.HTTP_200_OK
    assert await is_revoked_async("abc")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_revoke_returns_200_for_unknown_token(
    enable_rfc7009, async_client: AsyncClient
):
    """RFC 7009 §2.2: Endpoint must return HTTP 200 even for unknown tokens."""
    resp = await async_client.post(
        "/revoke", data={"token": "nonexistent"}
    )
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.unit
@pytest.mark.asyncio
async def test_revoke_returns_404_when_disabled(monkeypatch, async_client: AsyncClient):
    """RFC 7009: Revocation endpoint is unavailable when support is disabled."""
    monkeypatch.setattr(settings, "enable_rfc7009", False)
    await reset_revocations_async()
    resp = await async_client.post("/revoke", data={"token": "abc"})
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert not await is_revoked_async("abc")
