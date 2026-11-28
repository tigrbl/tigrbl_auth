"""RFC 8414 request orchestration without HTTP route ownership."""

from tigrbl.runtime.status import HTTPException, status
from tba_protocol_oauth.standards.authorization_server_metadata import (
    RFC8414_METADATA_PATH,
    RFC8414_SPEC_URL,
)
from tba_protocol_oidc.standards.discovery_metadata import build_openid_config
from tba_runtime_identity.deployment import deployment_from_request
from tba_runtime_identity.settings import settings


async def authorization_server_metadata(request: object) -> dict[str, object]:
    deployment = deployment_from_request(request, settings)
    if not settings.enable_rfc8414 or not deployment.route_enabled(
        RFC8414_METADATA_PATH
    ):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"RFC 8414 disabled: {RFC8414_SPEC_URL}",
        )
    return build_openid_config(deployment)


__all__ = ["authorization_server_metadata"]
