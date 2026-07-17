"""Runtime composition for the OpenID Connect UserInfo HTTP carrier."""

from tigrbl import TigrblApp
from tigrbl_auth_router_oidc_userinfo import (
    build_userinfo_router,
    include_userinfo_endpoint,
)
from tigrbl_identity_runtime.deployment import deployment_from_app
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage_runtime.engine import get_db

from .userinfo_runtime import first_user_by_filters, userinfo


router = build_userinfo_router(userinfo_request=userinfo, get_db=get_db)
api = router


def include_oidc_userinfo(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_userinfo_endpoint(
        app,
        router,
        enabled=deployment.route_enabled("/userinfo"),
    )


__all__ = [
    "api",
    "first_user_by_filters",
    "include_oidc_userinfo",
    "router",
    "userinfo",
]
