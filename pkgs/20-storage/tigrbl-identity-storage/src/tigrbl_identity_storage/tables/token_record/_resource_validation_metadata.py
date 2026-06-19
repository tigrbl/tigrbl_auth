"""Resource-validation metadata endpoints for protected APIs."""

from __future__ import annotations

from tigrbl_identity_runtime.deployment import deployment_from_app, deployment_from_request
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.framework import Request, TigrblApp, TigrblRouter
from tigrbl_authz_resource_server.runtime_metadata import (
    build_capability_attestation,
    runtime_truth_manifest,
)
from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import (
    build_protected_resource_verifier_contract,
)

CAPABILITIES_METADATA_PATH = "/metadata/capabilities"
VERIFIER_CONTRACT_METADATA_PATH = "/metadata/verifier-contract"

api = TigrblRouter()
router = api


@api.route(CAPABILITIES_METADATA_PATH, methods=["GET"], include_in_schema=True, tags=["metadata"])
async def capability_metadata(request: Request):
    deployment = deployment_from_request(request, settings)
    attestation = build_capability_attestation(deployment)
    return {
        **attestation.as_dict(),
        "runtime_truth": runtime_truth_manifest(deployment),
    }


@api.route(VERIFIER_CONTRACT_METADATA_PATH, methods=["GET"], include_in_schema=True, tags=["metadata"])
async def verifier_contract_metadata(request: Request):
    deployment = deployment_from_request(request, settings)
    return build_protected_resource_verifier_contract(deployment).as_metadata_projection()


def include_resource_validation_metadata(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    if deployment.product_surface != "resource-validation-api":
        return
    existing = {
        getattr(route, "path", None) or getattr(route, "path_template", None)
        for route in getattr(getattr(app, "router", None), "routes", [])
    }
    if CAPABILITIES_METADATA_PATH not in existing:
        app.include_router(api)


__all__ = [
    "CAPABILITIES_METADATA_PATH",
    "VERIFIER_CONTRACT_METADATA_PATH",
    "api",
    "capability_metadata",
    "include_resource_validation_metadata",
    "router",
    "verifier_contract_metadata",
]
