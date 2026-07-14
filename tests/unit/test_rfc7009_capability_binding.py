from __future__ import annotations

import pytest

from tigrbl_auth_protocol_oauth import CAPABILITY_REQUIREMENTS
from tigrbl_auth_protocol_oauth.standards.revocation import (
    RFC7009RevocationService,
    RevocationDisabledError,
)
from tigrbl_token_revocation_capability import TokenRevocationCapability


def test_rfc7009_maps_wire_operation_to_revocation_capability() -> None:
    requirement = next(
        item
        for item in CAPABILITY_REQUIREMENTS
        if item.protocol == "oauth-token-revocation"
    )

    assert requirement.revision == "RFC7009"
    assert requirement.wire_element == "/revoke"
    assert requirement.capability_id == "token.revocation"
    assert requirement.operation == "revoke_token"
    assert requirement.normalized_namespace == "oauth:rfc7009"


@pytest.mark.asyncio
async def test_rfc7009_service_invokes_capability_for_unknown_tokens() -> None:
    calls: list[tuple[str, str | None, str]] = []

    async def revoke(token: str, hint: str | None, reason: str) -> str:
        calls.append((token, hint, reason))
        return "digest:unknown"

    service = RFC7009RevocationService(TokenRevocationCapability(revoke))
    result = await service.revoke("unknown", token_type_hint="access_token")

    assert result.revoked is True
    assert calls == [("unknown", "access_token", "revoked_via_endpoint")]


@pytest.mark.asyncio
async def test_rfc7009_service_uses_composition_owned_feature_state() -> None:
    service = RFC7009RevocationService(
        TokenRevocationCapability(lambda token, hint, reason: "digest"),
        enabled=False,
    )

    with pytest.raises(RevocationDisabledError, match="RFC 7009"):
        await service.revoke("opaque-token")
