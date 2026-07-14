from __future__ import annotations

import pytest

from tigrbl_identity_contracts.oauth import PushedAuthorizationPersistenceRequest
from tigrbl_pushed_authorization_capability import PushedAuthorizationCapability


def test_pushed_authorization_requires_durable_target() -> None:
    with pytest.raises(NotImplementedError, match="push_authorization_request"):
        PushedAuthorizationCapability(None)


@pytest.mark.asyncio
async def test_pushed_authorization_delegates_persistence_and_audit() -> None:
    events: list[dict[str, object]] = []

    async def persist(request):
        return {
            "request_uri": "urn:ietf:params:oauth:request_uri:abc",
            "expires_in": 90,
            "record_id": "par-1",
        }

    capability = PushedAuthorizationCapability(persist, events.append)
    result = await capability.push(
        PushedAuthorizationPersistenceRequest(
            client_id="client-1",
            tenant_id="tenant-1",
            params={"scope": "openid"},
        )
    )

    assert result.request_uri.endswith(":abc")
    assert result.expires_in == 90
    assert events == [
        {
            "event_type": "authorization.par.created",
            "target_type": "par_request",
            "target_id": "par-1",
            "client_id": "client-1",
            "tenant_id": "tenant-1",
            "details": {"request_uri": result.request_uri},
        }
    ]
