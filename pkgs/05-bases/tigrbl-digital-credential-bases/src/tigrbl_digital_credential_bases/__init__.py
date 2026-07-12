from abc import ABC

from tigrbl_identity_contracts.digital_credentials import (
    CredentialFormatVerifierPort,
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
    CredentialIssuerPort,
    CredentialStatusReference,
    CredentialStatusResolverPort,
    CredentialVerificationRequest,
    CredentialVerificationResult,
    PresentationRequest,
    PresentationResult,
    PresentationVerifierPort,
    WalletAttestationVerifierPort,
)


class CredentialFormatBase(ABC):
    format_identifier: str


class CredentialIssuerBase(CredentialIssuerPort, ABC):
    def issue(self, request: CredentialIssuanceRequest, /) -> CredentialIssuanceResult:
        raise NotImplementedError


class CredentialVerifierBase(CredentialFormatVerifierPort, ABC):
    def verify(
        self, request: CredentialVerificationRequest, /
    ) -> CredentialVerificationResult:
        raise NotImplementedError


class PresentationVerifierBase(PresentationVerifierPort, ABC):
    def verify(
        self, presentation: bytes | str, request: PresentationRequest, /
    ) -> PresentationResult:
        raise NotImplementedError


class CredentialStatusResolverBase(CredentialStatusResolverPort, ABC):
    def resolve(self, reference: CredentialStatusReference, /) -> str:
        raise NotImplementedError


class WalletAttestationVerifierBase(WalletAttestationVerifierPort, ABC):
    def verify_wallet_attestation(self, attestation: bytes | str, /) -> bool:
        raise NotImplementedError


__all__ = [
    "CredentialFormatBase",
    "CredentialIssuerBase",
    "CredentialStatusResolverBase",
    "CredentialVerifierBase",
    "PresentationVerifierBase",
    "WalletAttestationVerifierBase",
]
