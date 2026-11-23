from __future__ import annotations

from types import SimpleNamespace

import pytest

from tba_router_oauth_introspection.binding import (
    _request_form_data,
    build_introspection_router,
)
from tba_protocol_oauth.standards.introspection import (
    RFC7662IntrospectionService,
)
from tba_capability_token_introspection import TokenIntrospectionCapability


@pytest.mark.asyncio
async def test_http_binding_materializes_urlencoded_form_data() -> None:
    request = SimpleNamespace(body=b"token=opaque-token&token_type_hint=access_token")

    assert await _request_form_data(request) == {
        "token": "opaque-token",
        "token_type_hint": "access_token",
    }


def test_http_binding_builds_post_introspection_carrier() -> None:
    service = RFC7662IntrospectionService(
        TokenIntrospectionCapability(lambda token: {"active": False})
    )

    router = build_introspection_router(
        service_for_request=lambda request: service,
        authorize_caller=lambda request, form, db: None,
        require_transport=lambda request: None,
        get_db=lambda: object(),
    )

    route = next(
        item
        for item in router.routes
        if getattr(item, "path", None) == "/introspect"
    )
    assert "POST" in route.methods
