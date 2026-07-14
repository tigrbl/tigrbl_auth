from __future__ import annotations

import pytest

from tigrbl_identity_contracts.oauth.exchange import (
    TokenExchangeContext,
    TokenExchangeRequest,
    TokenExchangeResponse,
    TokenExchangeSenderConstraint,
)
from tigrbl_token_exchange_capability import TokenExchangeCapability


def _context() -> TokenExchangeContext:
    return TokenExchangeContext(
        issuer="https://issuer.example",
        protected_resource_identifier="https://resource.example",
        sender_constraint=TokenExchangeSenderConstraint(
            mechanism="bearer",
            token_type="Bearer",
        ),
        verifier_logic_id="resource-verifier:test",
        required_claims=("iss", "sub", "aud"),
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_token_exchange_capability_delegates_typed_request() -> None:
    captured: dict[str, object] = {}

    async def exchange(request, context):
        captured["request"] = request
        captured["context"] = context
        return TokenExchangeResponse(
            access_token="issued-token",
            issued_token_type="urn:ietf:params:oauth:token-type:access_token",
            token_type="Bearer",
            audience=request.audience,
        )

    capability = TokenExchangeCapability(exchange)
    request = TokenExchangeRequest(
        subject_token="subject-token",
        subject_token_type="urn:ietf:params:oauth:token-type:access_token",
        audience="https://resource.example",
    )

    result = await capability.exchange(request, context=_context())

    assert result.access_token == "issued-token"
    assert captured == {"request": request, "context": _context()}
    assert capability.capability_report()["bound_operations"] == (
        "exchange_token",
    )


@pytest.mark.unit
def test_token_exchange_contract_requires_actor_token_type_pair() -> None:
    with pytest.raises(ValueError, match="supplied together"):
        TokenExchangeRequest(
            subject_token="subject-token",
            subject_token_type="urn:ietf:params:oauth:token-type:access_token",
            actor_token="actor-token",
        )


@pytest.mark.unit
def test_token_exchange_capability_rejects_missing_required_target() -> None:
    with pytest.raises(NotImplementedError, match="exchange_token"):
        TokenExchangeCapability(None)
