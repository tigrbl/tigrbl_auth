from __future__ import annotations

import pytest

from tigrbl_auth_protocol_oauth.capability_requirements import (
    CAPABILITY_REQUIREMENTS,
)
from tigrbl_auth_protocol_oauth.standards.token_endpoint import (
    RFC6749TokenEndpointService,
    TokenEndpointDisabledError,
)
from tigrbl_identity_contracts.tokens import (
    IssuedTokenPair,
    RefreshTokenRedemptionRequest,
    TokenPairIssueRequest,
)
from tigrbl_token_issuance_capability import TokenIssuanceCapability


def _issue_request() -> TokenPairIssueRequest:
    return TokenPairIssueRequest(
        subject="subject-1",
        tenant_id="tenant-1",
        client_id="client-1",
        issuer="https://issuer.example",
        scope="openid profile",
        audience="https://resource.example",
        confirmation={"jkt": "thumbprint"},
    )


def _refresh_request() -> RefreshTokenRedemptionRequest:
    return RefreshTokenRedemptionRequest(
        refresh_token="refresh-1",
        client_id="client-1",
        requested_audience="https://resource.example",
        token_type="DPoP",
    )


@pytest.mark.asyncio
async def test_token_issuance_capability_delegates_and_reports_operations() -> None:
    events: list[dict[str, object]] = []
    capability = TokenIssuanceCapability(
        lambda request: IssuedTokenPair("access-1", "refresh-1", "DPoP"),
        lambda request: IssuedTokenPair("access-2", "refresh-2", request.token_type),
        lambda event: events.append(dict(event)),
    )

    issued = await capability.call("issue_token_pair", _issue_request())
    refreshed = await capability.call("redeem_refresh_token", _refresh_request())

    assert issued.value.access_token == "access-1"
    assert refreshed.value.refresh_token == "refresh-2"
    assert capability.capability_report()["bound_operations"] == (
        "issue_token_pair",
        "record_audit_event",
        "redeem_refresh_token",
    )
    assert [event["event_type"] for event in events] == [
        "token.pair.issued",
        "token.refresh.rotated",
    ]


def test_token_issuance_capability_rejects_missing_required_target() -> None:
    with pytest.raises(NotImplementedError, match="redeem_refresh_token"):
        TokenIssuanceCapability(lambda request: IssuedTokenPair("access", None), None)


@pytest.mark.asyncio
async def test_rfc6749_service_maps_issuance_and_refresh() -> None:
    capability = TokenIssuanceCapability(
        lambda request: IssuedTokenPair("access-1", "refresh-1"),
        lambda request: IssuedTokenPair("access-2", "refresh-2"),
    )
    service = RFC6749TokenEndpointService(capability)
    assert (await service.issue(_issue_request())).access_token == "access-1"
    assert (await service.refresh(_refresh_request())).access_token == "access-2"
    with pytest.raises(TokenEndpointDisabledError):
        await RFC6749TokenEndpointService(capability, enabled=False).issue(
            _issue_request()
        )


def test_rfc6749_requirements_map_issuance_and_refresh_operations() -> None:
    operations = {
        requirement.operation
        for requirement in CAPABILITY_REQUIREMENTS
        if requirement.protocol == "oauth-token-endpoint"
    }
    assert operations == {"issue_token_pair", "redeem_refresh_token"}
