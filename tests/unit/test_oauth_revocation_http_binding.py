from __future__ import annotations

from types import SimpleNamespace

import pytest

from tigrbl_auth_router_oauth_revocation.binding import (
    _request_form_data,
    build_revocation_router,
)
from tigrbl_auth_protocol_oauth.standards.revocation import (
    RFC7009RevocationService,
)
from tigrbl_token_revocation_capability import TokenRevocationCapability


@pytest.mark.asyncio
async def test_revocation_binding_materializes_urlencoded_form_data() -> None:
    request = SimpleNamespace(
        body=b"token=opaque-token&token_type_hint=access_token"
    )

    assert await _request_form_data(request) == {
        "token": "opaque-token",
        "token_type_hint": "access_token",
    }


def test_revocation_binding_builds_post_revoke_carrier() -> None:
    service = RFC7009RevocationService(
        TokenRevocationCapability(lambda token, hint, reason: "digest")
    )
    router = build_revocation_router(
        service_for_request=lambda request: service,
    )

    route = next(
        item for item in router.routes if getattr(item, "path", None) == "/revoke"
    )
    assert "POST" in route.methods
