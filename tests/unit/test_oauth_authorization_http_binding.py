from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient
from tigrbl import RedirectResponse, TigrblApp
from tigrbl_auth_router_oauth_authorization import (
    build_authorization_router,
    include_authorization_endpoint,
)


def _router(target):
    return build_authorization_router(
        authorize_request=target,
        get_db=lambda: object(),
    )


def test_http_binding_builds_get_authorization_carrier() -> None:
    async def authorize_request(*, request, db, params):
        return RedirectResponse("https://client.example/callback")

    router = _router(authorize_request)
    route = next(
        item for item in router.routes if getattr(item, "path", None) == "/authorize"
    )

    assert route.methods == {"GET"}


@pytest.mark.asyncio
async def test_http_binding_materializes_authorization_query_once() -> None:
    observed = []

    async def authorize_request(*, request, db, params):
        observed.append(params)
        return RedirectResponse("https://client.example/callback?code=issued")

    app = TigrblApp()
    app.include_router(_router(authorize_request))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.get(
            "/authorize",
            params=[
                ("response_type", "code"),
                ("client_id", "client-1"),
                ("redirect_uri", "https://client.example/callback"),
                ("scope", "openid profile"),
                ("request", "signed-request-object"),
                ("resource", "api-a"),
                ("resource", "api-b"),
            ],
            follow_redirects=False,
        )

    assert response.status_code in {302, 307}
    assert response.headers["location"].endswith("?code=issued")
    assert observed == [
        {
            "response_type": "code",
            "client_id": "client-1",
            "redirect_uri": "https://client.example/callback",
            "scope": "openid profile",
            "response_mode": None,
            "state": None,
            "nonce": None,
            "code_challenge": None,
            "code_challenge_method": None,
            "prompt": None,
            "max_age": None,
            "login_hint": None,
            "claims": None,
            "request_uri": None,
            "request": "signed-request-object",
            "authorization_details": None,
            "resource": ["api-a", "api-b"],
        }
    ]


def test_http_binding_mounts_authorization_carrier_once() -> None:
    async def authorize_request(*, request, db, params):
        return RedirectResponse("https://client.example/callback")

    router = _router(authorize_request)
    app = TigrblApp()
    include_authorization_endpoint(app, router)
    include_authorization_endpoint(app, router)

    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert paths.count("/authorize") == 1
