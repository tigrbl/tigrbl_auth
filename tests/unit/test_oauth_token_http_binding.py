from __future__ import annotations

from tigrbl import TigrblApp
from tigrbl_auth_api_oauth_token import (
    build_token_router,
    include_token_endpoint,
)


def test_http_binding_builds_post_token_carrier() -> None:
    async def token_request(*, request, db):
        return {
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "token_type": "bearer",
        }

    router = build_token_router(
        token_request=token_request,
        get_db=lambda: object(),
    )
    route = next(
        item for item in router.routes if getattr(item, "path", None) == "/token"
    )

    assert route.methods == {"POST"}


def test_http_binding_mounts_token_carrier_once() -> None:
    async def token_request(*, request, db):
        return {"access_token": "access-token", "token_type": "bearer"}

    router = build_token_router(
        token_request=token_request,
        get_db=lambda: object(),
    )
    app = TigrblApp()
    include_token_endpoint(app, router)
    include_token_endpoint(app, router)

    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert paths.count("/token") == 1
