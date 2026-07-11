"""Base classes for resource-server providers."""

from abc import ABC

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    ResourceRequirement,
    ResourceServerVerifierPort,
    VerificationResult,
)


class ResourceServerVerifierBase(ResourceServerVerifierPort, ABC):
    def verify_claims(self, claims: AccessTokenClaims, requirement: ResourceRequirement, **kwargs: object) -> VerificationResult:
        raise NotImplementedError

    def verify_token(self, token: str | AccessTokenClaims, requirement: ResourceRequirement, **kwargs: object) -> VerificationResult:
        raise NotImplementedError


__all__ = ["ResourceServerVerifierBase"]
