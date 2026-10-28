from abc import ABC

from tba_contracts_public_key_authentication import (
    AttestationStatementVerifierPort,
    AttestationTrustResult,
    AuthenticatorAttestation,
    AuthenticatorMetadataProviderPort,
    AuthenticatorMetadataResult,
)


class AttestationStatementVerifierBase(AttestationStatementVerifierPort, ABC):
    def verify(
        self, attestation: AuthenticatorAttestation, /
    ) -> AttestationTrustResult:
        raise NotImplementedError


class AuthenticatorMetadataProviderBase(AuthenticatorMetadataProviderPort, ABC):
    async def resolve(self, aaguid: bytes, /) -> AuthenticatorMetadataResult:
        raise NotImplementedError


__all__ = ["AttestationStatementVerifierBase", "AuthenticatorMetadataProviderBase"]
