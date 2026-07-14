from __future__ import annotations

import importlib.util

import pytest
from httpx import ASGITransport, AsyncClient
from tigrbl import TigrblApp
from tigrbl_auth_api_oauth_device_authorization import (
    build_device_authorization_router,
    include_device_authorization_endpoint,
)


def _result() -> dict[str, object]:
    return {
        "device_code": "device-code",
        "user_code": "ABCD-EFGH",
        "verification_uri": "https://issuer.example/device",
        "verification_uri_complete": (
            "https://issuer.example/device?user_code=ABCD-EFGH"
        ),
        "expires_in": 600,
        "interval": 5,
    }


def _router(target):
    return build_device_authorization_router(
        device_authorization_request=target,
        get_db=lambda: object(),
    )


def test_http_binding_builds_post_device_authorization_carrier() -> None:
    async def target(**kwargs):
        return _result()

    route = next(
        item
        for item in _router(target).routes
        if getattr(item, "path", None) == "/device_authorization"
    )

    assert route.methods == {"POST"}
    assert importlib.util.find_spec(
        "tigrbl_identity_storage_runtime.device_authorization"
    ) is None


@pytest.mark.asyncio
async def test_http_binding_preserves_form_body_and_database() -> None:
    database = object()
    observed = []

    async def target(*, request, db):
        body = request.body
        if callable(body):
            body = await body()
        observed.append((bytes(body).decode("utf-8"), db))
        return _result()

    router = build_device_authorization_router(
        device_authorization_request=target,
        get_db=lambda: database,
    )
    app = TigrblApp()
    app.include_router(router)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.post(
            "/device_authorization",
            content="client_id=client-1&resource=api-a&resource=api-b",
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

    assert response.status_code == 200
    assert response.json() == _result()
    assert "resource=api-a&resource=api-b" in observed[0][0]
    assert observed[0][1] is database


def test_http_binding_mounts_device_authorization_carrier_once() -> None:
    async def target(**kwargs):
        return _result()

    router = _router(target)
    app = TigrblApp()
    include_device_authorization_endpoint(app, router)
    include_device_authorization_endpoint(app, router)
    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert paths.count("/device_authorization") == 1
