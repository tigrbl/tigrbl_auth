"""HTTP carrier binding for RFC 8628 device authorization."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

from tigrbl import Depends, Request, TigrblApp, TigrblRouter
from tigrbl_auth_protocol_oauth.schemas import DeviceAuthorizationOut


DatabaseDependency: TypeAlias = Callable[..., object]
DeviceAuthorizationTarget: TypeAlias = Callable[..., Any | Awaitable[Any]]


def build_device_authorization_router(
    *,
    device_authorization_request: DeviceAuthorizationTarget,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build the RFC 8628 POST carrier around injected orchestration."""

    router = TigrblRouter()

    @router.route(
        "/device_authorization",
        methods=["POST"],
        response_model=DeviceAuthorizationOut,
    )
    async def device_authorization(
        request: Request,
        db: object = Depends(get_db),
    ) -> Any:
        return await device_authorization_request(request=request, db=db)

    return router


def include_device_authorization_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the device-authorization carrier once when enabled."""

    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/device_authorization"
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "DatabaseDependency",
    "DeviceAuthorizationTarget",
    "build_device_authorization_router",
    "include_device_authorization_endpoint",
]
