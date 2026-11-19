"""Runtime composition for the RFC 9728 HTTP carrier."""

from tigrbl import TigrblApp
from tba_router_oauth_protected_resource_metadata import (
    build_protected_resource_metadata_router,
    include_protected_resource_metadata,
)
from tba_protocol_oauth.standards.protected_resource_metadata import (
    PROTECTED_RESOURCE_METADATA_PATH,
)
from tba_runtime_identity.deployment import deployment_from_app
from tba_runtime_identity.settings import settings

from tba_server_identity.protected_resource_metadata_runtime import (
    protected_resource_metadata,
)


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
