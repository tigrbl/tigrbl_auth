"""Reusable signing bases."""

from abc import ABC

from tigrbl_protected_artifact_bases import (
    ProtectedArtifactVerifierBase,
    SecurityArtifactCodecBase,
    SecurityArtifactIssuerBase,
)
from tigrbl_security_trust_contracts import (
    ICapabilityProvider,
    ISigningProvider,
    SignRequest,
    SignResult,
    VerifySignatureRequest,
    VerifySignatureResult,
)


class SigningProviderBase(ISigningProvider, ICapabilityProvider, ABC):
    async def sign(self, request: SignRequest) -> SignResult:
        raise NotImplementedError

    async def verify_signature(self, request: VerifySignatureRequest) -> VerifySignatureResult:
        raise NotImplementedError


class SigningDomainBase(
    ICapabilityProvider,
    SecurityArtifactIssuerBase,
    ProtectedArtifactVerifierBase,
    SecurityArtifactCodecBase,
    ABC,
):
    """Composite signing surface for artifact-oriented implementations."""


__all__ = ["SigningDomainBase", "SigningProviderBase"]
