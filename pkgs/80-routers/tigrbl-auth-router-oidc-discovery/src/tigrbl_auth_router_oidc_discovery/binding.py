"""HTTP routes for OIDC discovery and JWKS publication."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from tigrbl import Depends, Request, TigrblApp, TigrblRouter
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    JWKS_PATH,
)
from tigrbl_auth_protocol_oidc.tenant_discovery import (
    REALM_JWKS_PATH,
    REALM_OPENID_CONFIGURATION_PATH,
    TENANT_JWKS_PATH,
    TENANT_OPENID_CONFIGURATION_PATH,
)


OPENID_CONFIGURATION_PATH = "/.well-known/openid-configuration"


def build_oidc_discovery_routers(
    *,
    openid_configuration: Callable[..., Any],
    tenant_openid_configuration: Callable[..., Any],
    realm_openid_configuration: Callable[..., Any],
    jwks: Callable[..., Any],
    tenant_jwks: Callable[..., Any],
    realm_jwks: Callable[..., Any],
    get_db: Callable[..., object],
) -> tuple[TigrblRouter, TigrblRouter]:
    """Build discovery and JWKS carriers around injected orchestration."""

    discovery_router = TigrblRouter()
    jwks_router = TigrblRouter()

    @discovery_router.route(
        OPENID_CONFIGURATION_PATH,
        methods=["GET"],
        tags=[".well-known"],
    )
    async def issuer_configuration(request: Request):
        return await openid_configuration(request)

    @discovery_router.route(
        OPENID_CONFIGURATION_PATH,
        methods=["POST", "PUT", "PATCH", "DELETE"],
        include_in_schema=False,
        tags=[".well-known"],
    )
    async def issuer_configuration_method_not_allowed(request: Request):
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, "method not allowed")

    @discovery_router.route(
        TENANT_OPENID_CONFIGURATION_PATH,
        methods=["GET"],
        tags=[".well-known", "tenant"],
    )
    async def tenant_configuration(
        request: Request,
        tenant_slug: str,
        db=Depends(get_db),
    ):
        return await tenant_openid_configuration(request, tenant_slug, db)

    @discovery_router.route(
        REALM_OPENID_CONFIGURATION_PATH,
        methods=["GET"],
        tags=[".well-known", "realm"],
    )
    async def realm_configuration(
        request: Request,
        realm_slug: str,
        db=Depends(get_db),
    ):
        return await realm_openid_configuration(request, realm_slug, db)

    @jwks_router.route(JWKS_PATH, methods=["GET"], tags=[".well-known"])
    async def issuer_jwks(request: Request):
        return await jwks(request)

    @jwks_router.route(
        JWKS_PATH,
        methods=["POST", "PUT", "PATCH", "DELETE"],
        include_in_schema=False,
        tags=[".well-known"],
    )
    async def issuer_jwks_method_not_allowed(request: Request):
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, "method not allowed")

    @jwks_router.route(
        TENANT_JWKS_PATH,
        methods=["GET"],
        tags=[".well-known", "tenant"],
    )
    async def tenant_keys(
        request: Request,
        tenant_slug: str,
        db=Depends(get_db),
    ):
        return await tenant_jwks(request, tenant_slug, db)

    @jwks_router.route(
        REALM_JWKS_PATH,
        methods=["GET"],
        tags=[".well-known", "realm"],
    )
    async def realm_keys(
        request: Request,
        realm_slug: str,
        db=Depends(get_db),
    ):
        return await realm_jwks(request, realm_slug, db)

    return discovery_router, jwks_router


def _include_if_missing(
    app: TigrblApp,
    router: TigrblRouter,
    path: str,
    *,
    enabled: bool,
) -> None:
    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == path
        for route in routes
    ):
        app.include_router(router)


def include_openid_configuration(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool,
) -> None:
    _include_if_missing(app, router, OPENID_CONFIGURATION_PATH, enabled=enabled)


def include_jwks(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool,
) -> None:
    _include_if_missing(app, router, JWKS_PATH, enabled=enabled)


def include_oidc_discovery(
    app: TigrblApp,
    discovery_router: TigrblRouter,
    jwks_router: TigrblRouter,
    *,
    discovery_enabled: bool,
    jwks_enabled: bool,
) -> None:
    include_openid_configuration(
        app,
        discovery_router,
        enabled=discovery_enabled,
    )
    include_jwks(app, jwks_router, enabled=jwks_enabled)


__all__ = [
    "OPENID_CONFIGURATION_PATH",
    "build_oidc_discovery_routers",
    "include_jwks",
    "include_oidc_discovery",
    "include_openid_configuration",
]
