from __future__ import annotations

import importlib.util

import pytest
from httpx import ASGITransport, AsyncClient
from tigrbl import TigrblApp
from tigrbl_auth_router_session_login import (
    CredsIn,
    build_login_router,
    include_login_endpoint,
)


def _router(target):
    return build_login_router(login_request=target, get_db=lambda: object())


def test_http_binding_builds_post_login_carrier() -> None:
    async def login_request(**kwargs):
        return {"access_token": "access", "token_type": "bearer"}

    route = next(
        item
        for item in _router(login_request).routes
        if getattr(item, "path", None) == "/login"
    )

    assert route.methods == {"POST"}
    assert importlib.util.find_spec("tigrbl_identity_storage_runtime.login") is None


@pytest.mark.asyncio
async def test_http_binding_materializes_validated_credentials_once() -> None:
    database = object()
    observed = []

    async def login_request(*, request, db, identifier, password):
        observed.append((db, identifier, password))
        return {"access_token": "access", "token_type": "bearer"}

    router = build_login_router(
        login_request=login_request,
        get_db=lambda: database,
    )
    app = TigrblApp()
    app.include_router(router)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.post(
            "/login",
            json={"identifier": "alice", "password": "long-password"},
        )

    assert response.status_code == 200
    assert response.json() == {"access_token": "access", "token_type": "bearer"}
    assert observed == [(database, "alice", "long-password")]


def test_login_schema_and_mounting_remain_stable() -> None:
    assert CredsIn.model_json_schema()["required"] == ["identifier", "password"]

    async def login_request(**kwargs):
        return {"access_token": "access", "token_type": "bearer"}

    router = _router(login_request)
    app = TigrblApp()
    include_login_endpoint(app, router)
    include_login_endpoint(app, router)
    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert paths.count("/login") == 1
