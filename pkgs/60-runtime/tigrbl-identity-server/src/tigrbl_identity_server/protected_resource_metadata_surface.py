"""Runtime composition for the RFC 9728 HTTP carrier."""

from tigrbl import TigrblApp
from tigrbl_auth_router_oauth_protected_resource_metadata import (
    build_protected_resource_metadata_router,
    include_protected_resource_metadata,
)
from tigrbl_auth_protocol_oauth.standards.protected_resource_metadata import (
    PROTECTED_RESOURCE_METADATA_PATH,
)
from tigrbl_identity_runtime.deployment import deployment_from_app
from tigrbl_identity_runtime.settings import settings

from .protected_resource_metadata_runtime import protected_resource_metadata


router = build_protected_resource_metadata_router(
    protected_resource_metadata=protected_resource_metadata,
)
api = router


def include_rfc9728(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_protected_resource_metadata(
        app,
        router,
        enabled=deployment.route_enabled(PROTECTED_RESOURCE_METADATA_PATH),
    )


__all__ = ["api", "include_rfc9728", "router"]
