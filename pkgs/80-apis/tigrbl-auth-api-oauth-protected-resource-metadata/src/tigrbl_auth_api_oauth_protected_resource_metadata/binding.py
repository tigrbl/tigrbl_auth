"""HTTP carrier for RFC 9728 protected-resource metadata."""

from collections.abc import Callable
from typing import Any

from tigrbl import Request, TigrblApp, TigrblRouter
from tigrbl_auth_protocol_oauth.standards.protected_resource_metadata import (
    PROTECTED_RESOURCE_METADATA_PATH,
)


def build_protected_resource_metadata_router(
    *,
    protected_resource_metadata: Callable[..., Any],
) -> TigrblRouter:
    router = TigrblRouter()

    @router.route(
        PROTECTED_RESOURCE_METADATA_PATH,
        methods=["GET"],
        include_in_schema=True,
        tags=[".well-known"],
    )
    async def metadata(request: Request):
        return await protected_resource_metadata(request)

    return router


def include_protected_resource_metadata(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool,
) -> None:
    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == PROTECTED_RESOURCE_METADATA_PATH
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "build_protected_resource_metadata_router",
    "include_protected_resource_metadata",
]
