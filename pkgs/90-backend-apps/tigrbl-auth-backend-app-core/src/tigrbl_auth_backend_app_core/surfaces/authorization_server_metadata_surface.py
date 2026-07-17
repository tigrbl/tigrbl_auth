"""Runtime composition for the RFC 8414 HTTP carrier."""

from tigrbl import TigrblApp
from tigrbl_auth_router_oauth_authorization_server_metadata import (
    build_authorization_server_metadata_router,
    include_authorization_server_metadata,
)
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    RFC8414_METADATA_PATH,
)
from tigrbl_identity_runtime.deployment import deployment_from_app
from tigrbl_identity_runtime.settings import settings

from tigrbl_identity_server.authorization_server_metadata_runtime import (
    authorization_server_metadata,
)


router = build_authorization_server_metadata_router(
    authorization_server_metadata=authorization_server_metadata,
)
api = router


def include_rfc8414(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_authorization_server_metadata(
        app,
        router,
        enabled=(
            bool(settings.enable_rfc8414)
            and deployment.route_enabled(RFC8414_METADATA_PATH)
        ),
    )


__all__ = ["api", "include_rfc8414", "router"]
