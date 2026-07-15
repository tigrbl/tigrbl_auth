import asyncio

import pytest
from tigrbl_grant_negotiation_capability import GrantNegotiationCapability
from tigrbl_identity_contracts.gnap import (
    GrantAccessRequest,
    GrantContinuationRequest,
    GrantNegotiationRequest,
    GrantNegotiationResult,
)


def _request() -> GrantNegotiationRequest:
    return GrantNegotiationRequest(
        (GrantAccessRequest(("read",), label="read-token"),),
        "client-instance-1",
    )


def test_grant_capability_requires_request_target_and_reports_optionals() -> None:
    with pytest.raises(NotImplementedError):
        GrantNegotiationCapability(None)

    capability = GrantNegotiationCapability(
        lambda request: GrantNegotiationResult("grant-1", "pending")
    )

    assert capability.state().ready
    assert set(capability.callables()) == {"request_grant"}


def test_grant_capability_delegates_typed_request_continue_and_rotation() -> None:
    seen = []

    async def request_grant(request):
        seen.append(("request", request))
        return GrantNegotiationResult("grant-1", "pending")

    def continue_grant(request):
        seen.append(("continue", request))
        return GrantNegotiationResult("grant-1", "approved")

    capability = GrantNegotiationCapability(
        request_grant,
        continue_grant=continue_grant,
        rotate_access_token=lambda request: GrantNegotiationResult(
            "grant-1", "approved", ({"value": "rotated"},)
        ),
    )

    requested = asyncio.run(capability.request(_request()))
    continued = asyncio.run(
        capability.continue_request(GrantContinuationRequest("continue-token"))
    )
    rotated = asyncio.run(capability.rotate(GrantContinuationRequest("continue-token")))

    assert requested.status == "pending"
    assert continued.status == "approved"
    assert rotated.access_tokens == ({"value": "rotated"},)
    assert [kind for kind, _ in seen] == ["request", "continue"]
