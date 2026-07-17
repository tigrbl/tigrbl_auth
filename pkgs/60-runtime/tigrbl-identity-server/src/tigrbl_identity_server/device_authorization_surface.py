"""Runtime composition for the RFC 8628 device-authorization carrier."""

from tigrbl import TigrblApp
from tigrbl_auth_router_oauth_device_authorization import (
    build_device_authorization_router,
    include_device_authorization_endpoint as include_device_carrier,
)
from tigrbl_identity_runtime.deployment import deployment_from_app
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage_runtime.engine import get_db

from .device_authorization_runtime import (
    device_authorization,
    device_authorization_request,
)


router = build_device_authorization_router(
    device_authorization_request=device_authorization,
    get_db=get_db,
)
api = router


def include_device_authorization_endpoint(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_device_carrier(
        app,
        router,
        enabled=deployment.route_enabled("/device_authorization"),
    )


include_rfc8628 = include_device_authorization_endpoint


__all__ = [
    "api",
    "device_authorization",
    "device_authorization_request",
    "include_device_authorization_endpoint",
    "include_rfc8628",
    "router",
]
