from __future__ import annotations

import pytest

from tigrbl_auth_protocol_oauth import CAPABILITY_REQUIREMENTS
from tigrbl_auth_protocol_oauth.standards.rfc7662 import (
    IntrospectionDisabledError,
    RFC7662IntrospectionService,
)
from tigrbl_token_introspection_capability import TokenIntrospectionCapability


def test_rfc7662_maps_its_wire_operation_to_the_introspection_capability() -> None:
    requirement = next(
        item
        for item in CAPABILITY_REQUIREMENTS
        if item.protocol == "oauth-token-introspection"
    )

    assert requirement.revision == "RFC7662"
    assert requirement.wire_element == "/introspect"
    assert requirement.capability_id == "token.introspection"
    assert requirement.operation == "introspect_token"
    assert requirement.normalized_namespace == "oauth:rfc7662"


@pytest.mark.asyncio
async def test_rfc7662_service_applies_protocol_activity_constraints() -> None:
    capability = TokenIntrospectionCapability(
        lambda token: {
            "active": True,
            "sub": "subject-1",
            "authz_version": 1,
            "current_authz_version": 2,
        }
    )
    service = RFC7662IntrospectionService(capability)

    assert await service.introspect("opaque-token") == {
        "sub": "subject-1",
        "authz_version": 1,
        "current_authz_version": 2,
        "active": False,
        "inactive_reason": "authorization_snapshot_stale",
    }


@pytest.mark.asyncio
async def test_rfc7662_service_uses_composition_owned_feature_state() -> None:
    capability = TokenIntrospectionCapability(lambda token: {"active": False})
    service = RFC7662IntrospectionService(capability, enabled=False)

    with pytest.raises(IntrospectionDisabledError, match="RFC 7662"):
        await service.introspect("opaque-token")
