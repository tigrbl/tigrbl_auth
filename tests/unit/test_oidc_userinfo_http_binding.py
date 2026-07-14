from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient
from tigrbl import TigrblApp
from tigrbl_auth_api_oidc_userinfo import (
    build_userinfo_router,
    include_userinfo_endpoint,
)


def _router(target):
    return build_userinfo_router(
        userinfo_request=target,
        get_db=lambda: object(),
    )


def test_http_binding_builds_get_userinfo_carrier() -> None:
    async def userinfo_request(*, request, db):
        return {"sub": "user-1"}

    route = next(
        item
        for item in _router(userinfo_request).routes
        if getattr(item, "path", None) == "/userinfo"
    )

    assert route.methods == {"GET"}


@pytest.mark.asyncio
async def test_http_binding_delegates_request_and_database() -> None:
    database = object()
    observed = []

    async def userinfo_request(*, request, db):
        observed.append((request, db))
        return {"sub": "user-1", "name": "Alice"}

    router = build_userinfo_router(
        userinfo_request=userinfo_request,
        get_db=lambda: database,
    )
    app = TigrblApp()
    app.include_router(router)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.get(
            "/userinfo",
            headers={"Authorization": "Bearer access-token"},
        )

    assert response.status_code == 200
    assert response.json() == {"sub": "user-1", "name": "Alice"}
    assert len(observed) == 1
    assert observed[0][1] is database


def test_http_binding_mounts_userinfo_carrier_once() -> None:
    async def userinfo_request(*, request, db):
        return {"sub": "user-1"}

    router = _router(userinfo_request)
    app = TigrblApp()
    include_userinfo_endpoint(app, router)
    include_userinfo_endpoint(app, router)

    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert paths.count("/userinfo") == 1
