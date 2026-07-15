"""Resource-validation metadata orchestration without HTTP route ownership."""

from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import (
    build_protected_resource_verifier_contract,
)
from tigrbl_authz_resource_server.runtime_metadata import (
    build_capability_attestation,
    runtime_truth_manifest,
)
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_runtime.settings import settings


async def capability_metadata(request: object) -> dict[str, object]:
    deployment = deployment_from_request(request, settings)
    attestation = build_capability_attestation(deployment)
    return {
        **attestation.as_dict(),
        "runtime_truth": runtime_truth_manifest(deployment),
    }


async def verifier_contract_metadata(request: object) -> dict[str, object]:
    deployment = deployment_from_request(request, settings)
    return build_protected_resource_verifier_contract(
        deployment
    ).as_metadata_projection()


__all__ = ["capability_metadata", "verifier_contract_metadata"]
