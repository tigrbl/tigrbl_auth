"""Unit tests for the RFC 7662 protocol service."""

import pytest

from tigrbl_auth_protocol_oauth.standards.introspection import (
    IntrospectionDisabledError,
    RFC7662IntrospectionService,
)
from tigrbl_token_introspection_capability import TokenIntrospectionCapability


def _service(payload: dict[str, object], *, enabled: bool = True):
    return RFC7662IntrospectionService(
        TokenIntrospectionCapability(lambda token: payload),
        enabled=enabled,
    )


@pytest.mark.asyncio
async def test_introspect_active_token():
    result = await _service({"active": True, "sub": "alice"}).introspect(
        "tok123"
    )
    assert result == {"active": True, "sub": "alice"}


@pytest.mark.asyncio
async def test_introspect_stale_authorization_snapshot_is_inactive():
    result = await _service(
        {
            "active": True,
            "sub": "alice",
            "authz_version": 1,
            "current_authz_version": 2,
        }
    ).introspect("stale-authz")

    assert result["active"] is False
    assert result["inactive_reason"] == "authorization_snapshot_stale"


@pytest.mark.asyncio
async def test_introspect_inactive_token():
    assert await _service({"active": False}).introspect("missing") == {
        "active": False
    }


@pytest.mark.asyncio
async def test_introspection_disabled():
    with pytest.raises(IntrospectionDisabledError):
        await _service({"active": True}, enabled=False).introspect("tok123")
