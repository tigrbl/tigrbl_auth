"""Reusable certificate bases."""

from abc import ABC

from tigrbl_protected_artifact_bases import (
    ProtectedArtifactVerifierBase,
    SecurityArtifactCodecBase,
    SecurityArtifactIssuerBase,
)
from tigrbl_security_trust_contracts import (
    CertificatePathValidationRequest,
    CertificatePathValidationResult,
    CertificatePathValidatorPort,
    CertificateRequest,
    CertificateVerifyRequest,
    ICapabilityProvider,
    ParseRequest,
    ParsedArtifact,
    VerificationResult,
)


class CertificateServiceBase(
    ICapabilityProvider,
    SecurityArtifactIssuerBase,
    ProtectedArtifactVerifierBase,
    SecurityArtifactCodecBase,
    ABC,
):
    async def create_csr(self, request: CertificateRequest):
        raise NotImplementedError

    async def issue_certificate(self, request: CertificateRequest):
        raise NotImplementedError

    async def verify_certificate(self, request: CertificateVerifyRequest) -> VerificationResult:
        raise NotImplementedError

    async def parse_certificate(self, request: ParseRequest) -> ParsedArtifact:
        raise NotImplementedError


class CertificatePathValidatorBase(CertificatePathValidatorPort, ABC):
    def validate(self, request: CertificatePathValidationRequest, /) -> CertificatePathValidationResult:
        raise NotImplementedError


CertificateServiceDomainBase = CertificateServiceBase
CertificateDomainBase = CertificateServiceBase

__all__ = [
    "CertificateDomainBase",
    "CertificatePathValidatorBase",
    "CertificateServiceBase",
    "CertificateServiceDomainBase",
]
