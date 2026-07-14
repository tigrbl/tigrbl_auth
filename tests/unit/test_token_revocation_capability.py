from __future__ import annotations

import pytest

from tigrbl_identity_contracts.tokens import TokenRevocationRequest
from tigrbl_token_revocation_capability import TokenRevocationCapability


def test_revocation_capability_requires_durable_target() -> None:
    with pytest.raises(NotImplementedError, match="revoke_token"):
        TokenRevocationCapability(None)


@pytest.mark.asyncio
async def test_revocation_capability_delegates_durable_and_audit_operations() -> None:
    calls: list[object] = []

    async def revoke(token: str, hint: str | None, reason: str) -> str:
        calls.append((token, hint, reason))
        return "digest:abc"

    async def audit(event: dict[str, object]) -> None:
        calls.append(event)

    capability = TokenRevocationCapability(revoke, audit)
    call = await capability.call(
        "revoke_token",
        TokenRevocationRequest(
            "opaque-token",
            token_type_hint="access_token",
            reason="revoked_via_endpoint",
        ),
    )

    assert call.value.revoked is True
    assert call.value.token_reference == "digest:abc"
    assert calls[0] == (
        "opaque-token",
        "access_token",
        "revoked_via_endpoint",
    )
    assert calls[1] == {
        "event_type": "token.revoked",
        "target_type": "token",
        "target_id": "opaque-token",
        "details": {"token_type_hint": "access_token"},
    }
    assert capability.state().details == {"audit_bound": True}


def test_revocation_request_requires_token() -> None:
    with pytest.raises(ValueError, match="token is required"):
        TokenRevocationRequest("")
