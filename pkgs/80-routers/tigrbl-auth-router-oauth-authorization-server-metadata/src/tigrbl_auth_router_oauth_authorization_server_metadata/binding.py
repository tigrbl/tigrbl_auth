"""HTTP carrier for RFC 8414 authorization-server metadata."""

from collections.abc import Callable
from typing import Any

from tigrbl import Request, TigrblApp, TigrblRouter
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    RFC8414_METADATA_PATH,
)


def build_authorization_server_metadata_router(
    *,
    authorization_server_metadata: Callable[..., Any],
) -> TigrblRouter:
    router = TigrblRouter()

    @router.route(
        RFC8414_METADATA_PATH,
        methods=["GET"],
        include_in_schema=True,
        tags=[".well-known"],
    )
    async def metadata(request: Request):
        return await authorization_server_metadata(request)

    return router


def include_authorization_server_metadata(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool,
) -> None:
    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == RFC8414_METADATA_PATH
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "build_authorization_server_metadata_router",
    "include_authorization_server_metadata",
]
