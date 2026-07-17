"""HTTP carrier binding for RFC 7591 and RFC 7592 client registration."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import TypeAlias

from tigrbl import Depends, Request, TigrblApp, TigrblRouter
from tigrbl_auth_protocol_oauth.schemas import (
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
)


DatabaseDependency: TypeAlias = Callable[..., object]
RegisterTarget: TypeAlias = Callable[
    [Request, object, DynamicClientRegistrationIn],
    Mapping[str, object] | Awaitable[Mapping[str, object]],
]
GetRegistrationTarget: TypeAlias = Callable[
    [Request, object, str],
    Mapping[str, object] | Awaitable[Mapping[str, object]],
]
UpdateRegistrationTarget: TypeAlias = Callable[
    [Request, object, str, DynamicClientRegistrationManagementIn],
    Mapping[str, object] | Awaitable[Mapping[str, object]],
]
DeleteRegistrationTarget: TypeAlias = Callable[
    [Request, object, str],
    Mapping[str, object] | Awaitable[Mapping[str, object]],
]


def build_client_registration_router(
    *,
    register_client: RegisterTarget,
    get_registration: GetRegistrationTarget,
    update_registration: UpdateRegistrationTarget,
    delete_registration: DeleteRegistrationTarget,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build registration routes around injected runtime collaborators."""

    router = TigrblRouter()

    @router.route(
        "/register",
        methods=["POST"],
        response_model=DynamicClientRegistrationOut,
    )
    async def register(request: Request, db=Depends(get_db)):
        body = await request.json() if hasattr(request, "json") else {}
        payload = DynamicClientRegistrationIn(**body)
        return await register_client(request, db, payload)

    @router.route(
        "/register/{client_id}",
        methods=["GET"],
        response_model=DynamicClientRegistrationOut,
    )
    async def register_get(request: Request, client_id: str, db=Depends(get_db)):
        return await get_registration(request, db, client_id)

    @router.route(
        "/register/{client_id}",
        methods=["PUT"],
        response_model=DynamicClientRegistrationOut,
    )
    async def register_put(request: Request, client_id: str, db=Depends(get_db)):
        body = await request.json() if hasattr(request, "json") else {}
        payload = DynamicClientRegistrationManagementIn(**body)
        return await update_registration(request, db, client_id, payload)

    @router.route("/register/{client_id}", methods=["DELETE"])
    async def register_delete(
        request: Request,
        client_id: str,
        db=Depends(get_db),
    ):
        return await delete_registration(request, db, client_id)

    return router


def include_client_registration_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    registration_enabled: bool,
    management_enabled: bool,
) -> None:
    """Mount the shared registration carrier once when either RFC is enabled."""

    paths = ("/register", "/register/{client_id}")
    routes = getattr(getattr(app, "router", None), "routes", ())
    if (registration_enabled or management_enabled) and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        in paths
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "DatabaseDependency",
    "DeleteRegistrationTarget",
    "GetRegistrationTarget",
    "RegisterTarget",
    "UpdateRegistrationTarget",
    "build_client_registration_router",
    "include_client_registration_endpoint",
]
