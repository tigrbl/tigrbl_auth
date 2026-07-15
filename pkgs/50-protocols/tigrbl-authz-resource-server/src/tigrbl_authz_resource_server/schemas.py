"""Normalized protected-resource request and result schemas."""

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    FrameworkRequest,
    ResourceRequirement,
    VerificationResult,
    VerificationStatus,
    VerifierContractProfile,
)

from .metadata import verifier_contract_from_metadata

__all__ = [
    "AccessTokenClaims",
    "FrameworkRequest",
    "ResourceRequirement",
    "VerificationResult",
    "VerificationStatus",
    "VerifierContractProfile",
    "verifier_contract_from_metadata",
]
