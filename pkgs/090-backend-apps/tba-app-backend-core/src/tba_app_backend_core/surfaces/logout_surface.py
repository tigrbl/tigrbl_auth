"""Runtime composition for the OpenID Connect logout HTTP carrier."""

from tigrbl import TigrblApp
from tba_router_oidc_logout import (
    build_logout_router,
    include_logout_endpoint as include_logout_carrier,
)
from tba_runtime_identity.deployment import deployment_from_app
from tba_runtime_identity.settings import settings
from tba_runtime_identity_storage.engine import get_db

from tba_server_identity.logout_runtime import logout, logout_request


router = build_logout_router(logout_request=logout, get_db=get_db)
api = router


def include_logout_endpoint(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_logout_carrier(
        app,
        router,
        enabled=deployment.route_enabled("/logout"),
    )


include_oidc_rp_initiated_logout = include_logout_endpoint


__all__ = [
    "api",
    "include_logout_endpoint",
    "include_oidc_rp_initiated_logout",
    "logout",
    "logout_request",
    "router",
]
