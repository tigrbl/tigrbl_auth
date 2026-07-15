"""RFC 9728 request orchestration without HTTP route ownership."""

from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_protocol_oauth.standards.protected_resource_metadata import (
    PROTECTED_RESOURCE_METADATA_PATH,
    RFC9728_SPEC_URL,
    build_protected_resource_metadata,
)
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_runtime.settings import settings


async def protected_resource_metadata(request: object) -> dict[str, object]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(PROTECTED_RESOURCE_METADATA_PATH):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"RFC 9728 disabled: {RFC9728_SPEC_URL}",
        )
    return build_protected_resource_metadata(deployment)


__all__ = ["protected_resource_metadata"]
