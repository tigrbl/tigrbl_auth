"""Runtime composition for OIDC discovery and JWKS HTTP carriers."""

from tigrbl import TigrblApp, TigrblRouter
from tba_router_oidc_discovery import (
    build_oidc_discovery_routers,
    include_jwks as include_jwks_carrier,
    include_oidc_discovery as include_oidc_discovery_carrier,
    include_openid_configuration as include_openid_configuration_carrier,
)
from tba_protocol_oauth.standards.authorization_server_metadata import (
    JWKS_PATH,
)
from tba_runtime_identity.deployment import deployment_from_app
from tba_runtime_identity.settings import settings
from tba_runtime_identity_storage.engine import get_db

from tba_server_identity.oidc_discovery_runtime import (
    jwks,
    openid_configuration,
    realm_jwks,
    realm_openid_configuration,
    tenant_jwks,
    tenant_openid_configuration,
)


discovery_api, jwks_api = build_oidc_discovery_routers(
    openid_configuration=openid_configuration,
    tenant_openid_configuration=tenant_openid_configuration,
    realm_openid_configuration=realm_openid_configuration,
    jwks=jwks,
    tenant_jwks=tenant_jwks,
    realm_jwks=realm_jwks,
    get_db=get_db,
)
api = TigrblRouter()
api.include_router(discovery_api)
api.include_router(jwks_api)
router = api


def include_openid_configuration(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_openid_configuration_carrier(
        app,
        discovery_api,
        enabled=deployment.route_enabled("/.well-known/openid-configuration"),
    )


def include_jwks(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_jwks_carrier(
        app,
        jwks_api,
        enabled=deployment.route_enabled(JWKS_PATH),
    )


def include_oidc_discovery(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_oidc_discovery_carrier(
        app,
        discovery_api,
        jwks_api,
        discovery_enabled=deployment.route_enabled("/.well-known/openid-configuration"),
        jwks_enabled=deployment.route_enabled(JWKS_PATH),
    )


__all__ = [
    "api",
    "discovery_api",
    "include_jwks",
    "include_oidc_discovery",
    "include_openid_configuration",
    "jwks_api",
    "router",
]
