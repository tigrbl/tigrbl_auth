"""Reusable signing bases."""

from abc import ABC

from tba_bases_protected_artifact import (
    ProtectedArtifactVerifierBase,
    SecurityArtifactCodecBase,
    SecurityArtifactIssuerBase,
)
from tba_contracts_security_trust import (
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
