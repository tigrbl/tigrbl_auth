"""Tests for the RFC 7662 HTTP carrier and protocol service."""

from http import HTTPStatus as status

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl import TigrblApp
from tigrbl_auth_router_oauth_introspection import build_introspection_router
from tigrbl_auth_protocol_oauth.standards.introspection import (
    RFC7662IntrospectionService,
)
from tigrbl_token_introspection_capability import TokenIntrospectionCapability


def _router(*, authorized: bool = True):
    async def authorize(request, form, db):
        if not authorized:
            from tigrbl.runtime.status import HTTPException

            raise HTTPException(status.UNAUTHORIZED, "invalid_client")

    service = RFC7662IntrospectionService(
        TokenIntrospectionCapability(
            lambda token: {"active": token == "dummy"}
        )
    )
    return build_introspection_router(
        service_for_request=lambda request: service,
        authorize_caller=authorize,
        require_transport=lambda request: None,
        get_db=lambda: object(),
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_introspection_endpoint_returns_active_field():
    app = TigrblApp()
    app.include_router(_router())

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://test"
    ) as client:
        response = await client.post("/introspect", data={"token": "dummy"})

    assert response.status_code == status.OK
    assert response.json() == {"active": True}


@pytest.mark.unit
@pytest.mark.asyncio
async def test_introspection_requires_token_parameter():
    app = TigrblApp()
    app.include_router(_router())

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://test"
    ) as client:
        response = await client.post("/introspect", data={})

    assert response.status_code == status.BAD_REQUEST


@pytest.mark.unit
@pytest.mark.asyncio
async def test_introspection_requires_authenticated_caller():
    app = TigrblApp()
    app.include_router(_router(authorized=False))

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://test"
    ) as client:
        response = await client.post("/introspect", data={"token": "dummy"})

    assert response.status_code == status.UNAUTHORIZED
