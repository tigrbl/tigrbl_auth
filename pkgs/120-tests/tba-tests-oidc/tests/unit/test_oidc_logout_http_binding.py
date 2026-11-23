from __future__ import annotations

from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from tigrbl import TigrblApp
from tba_protocol_oidc.standards.rp_initiated_logout import (
    validate_post_logout_redirect_uri,
)
from tba_router_oidc_logout import (
    build_logout_router,
    include_logout_endpoint,
)


def _router(target):
    return build_logout_router(logout_request=target, get_db=lambda: object())


def test_http_binding_builds_get_and_post_logout_carriers() -> None:
    async def logout_request(*, request, db):
        return {"status": "logged_out"}

    route = next(
        item
        for item in _router(logout_request).routes
        if getattr(item, "path", None) == "/logout"
    )

    assert route.methods == {"GET", "POST"}


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "POST"])
async def test_http_binding_delegates_each_logout_method(method: str) -> None:
    observed = []

    async def logout_request(*, request, db):
        observed.append((request.method, db))
        return {"status": "logged_out"}

    app = TigrblApp()
    app.include_router(_router(logout_request))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.request(method, "/logout")

    assert response.status_code == 200
    assert response.json() == {"status": "logged_out"}
    assert observed[0][0] == method


def test_http_binding_mounts_logout_carrier_once() -> None:
    async def logout_request(*, request, db):
        return {"status": "logged_out"}

    router = _router(logout_request)
    app = TigrblApp()
    include_logout_endpoint(app, router)
    include_logout_endpoint(app, router)

    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert paths.count("/logout") == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "return_uri", ["http://rp.example/callback", "https://rp.example/unregistered"]
)
async def test_http_binding_rejects_unregistered_logout_redirect(return_uri: str) -> None:
    async def logout_request(*, request, db):
        return await validate_post_logout_redirect_uri(
            client_id=uuid4(),
            post_logout_redirect_uri=return_uri,
            registration_metadata={
                "post_logout_redirect_uris": ["https://rp.example/callback"]
            },
        )

    app = TigrblApp()
    app.include_router(_router(logout_request))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.get("/logout")

    assert response.status_code == 400
    assert "location" not in response.headers
