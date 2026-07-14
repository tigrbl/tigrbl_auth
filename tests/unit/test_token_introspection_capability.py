from __future__ import annotations

import pytest

from tigrbl_identity_contracts.tokens import (
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
    TokenProfile,
)
from tigrbl_token_introspection_capability import TokenIntrospectionCapability


def test_introspection_capability_requires_a_bound_target() -> None:
    with pytest.raises(NotImplementedError, match="introspect_token"):
        TokenIntrospectionCapability(None)


@pytest.mark.asyncio
async def test_introspection_capability_normalizes_durable_mapping() -> None:
    async def introspect(token: str) -> dict[str, object]:
        assert token == "opaque-token"
        return {
            "active": True,
            "sub": "subject-1",
            "token_profile": TokenProfile.ACCESS_TOKEN.value,
        }

    capability = TokenIntrospectionCapability(introspect)
    call = await capability.call(
        "introspect_token",
        TokenIntrospectionRequest(
            "opaque-token",
            expected_profile=TokenProfile.ACCESS_TOKEN,
        ),
    )

    assert call.capability_id == "token.introspection"
    assert call.operation == "introspect_token"
    assert call.delegated is True
    assert call.value == TokenIntrospectionResult(
        active=True,
        claims={
            "sub": "subject-1",
            "token_profile": TokenProfile.ACCESS_TOKEN.value,
        },
        profile=TokenProfile.ACCESS_TOKEN,
    )
    assert capability.capability_report()["bound_operations"] == (
        "introspect_token",
    )
    assert capability.state().ready is True


@pytest.mark.asyncio
async def test_introspection_capability_fails_closed_on_profile_mismatch() -> None:
    capability = TokenIntrospectionCapability(
        lambda token: {
            "active": True,
            "sub": "subject-1",
            "token_profile": TokenProfile.REFRESH_TOKEN.value,
        }
    )

    result = await capability.introspect_token(
        TokenIntrospectionRequest(
            "opaque-token",
            expected_profile=TokenProfile.ACCESS_TOKEN,
        )
    )

    assert result.active is False
    assert result.profile is TokenProfile.REFRESH_TOKEN
    assert result.reason == "token profile mismatch"
    assert result.claims == {}


@pytest.mark.asyncio
async def test_introspection_capability_rejects_untyped_target_result() -> None:
    capability = TokenIntrospectionCapability(lambda token: object())

    with pytest.raises(TypeError, match="must return"):
        await capability.introspect_token(TokenIntrospectionRequest("opaque-token"))


def test_introspection_request_rejects_empty_token() -> None:
    with pytest.raises(ValueError, match="token is required"):
        TokenIntrospectionRequest("")
