from __future__ import annotations

import pytest

from tba_protocol_oauth import CAPABILITY_REQUIREMENTS
from tba_protocol_oauth.standards.pushed_authorization_requests import (
    PushedAuthorizationDisabledError,
    RFC9126PushedAuthorizationService,
)
from tba_capability_authorization_request_staging import PushedAuthorizationCapability


def test_rfc9126_maps_wire_operation_to_pushed_authorization_capability() -> None:
    requirement = next(
        item
        for item in CAPABILITY_REQUIREMENTS
        if item.protocol == "oauth-pushed-authorization"
    )

    assert requirement.revision == "RFC9126"
    assert requirement.wire_element == "/par"
    assert requirement.capability_id == "oauth.pushed-authorization"
    assert requirement.operation == "push_authorization_request"
    assert requirement.normalized_namespace == "oauth:rfc9126"


@pytest.mark.asyncio
async def test_rfc9126_service_invokes_capability_with_normalized_input() -> None:
    requests = []

    async def persist(request):
        requests.append(request)
        return {
            "request_uri": "urn:ietf:params:oauth:request_uri:abc",
            "expires_in": 90,
            "record_id": "par-1",
        }

    service = RFC9126PushedAuthorizationService(
        PushedAuthorizationCapability(persist)
    )
    result = await service.push(
        client_id="client-1",
        tenant_id="tenant-1",
        params={"scope": "openid"},
    )

    assert result.record_id == "par-1"
    assert requests[0].params == {"scope": "openid"}


@pytest.mark.asyncio
async def test_rfc9126_service_uses_composition_owned_feature_state() -> None:
    service = RFC9126PushedAuthorizationService(
        PushedAuthorizationCapability(
            lambda request: {
                "request_uri": "urn:ietf:params:oauth:request_uri:unused",
                "expires_in": 90,
            }
        ),
        enabled=False,
    )

    with pytest.raises(PushedAuthorizationDisabledError, match="RFC 9126"):
        await service.push(client_id="client-1", tenant_id=None, params={})
