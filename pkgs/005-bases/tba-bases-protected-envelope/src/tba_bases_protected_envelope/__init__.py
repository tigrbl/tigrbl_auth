from abc import ABC
from tba_contracts_protected_envelope import EnvelopeProtectionRequest, EnvelopeVerificationRequest, EnvelopeVerificationResult, ProtectedEnvelope, ProtectedEnvelopeIssuerPort, ProtectedEnvelopeVerifierPort, VerificationKeyRequest, VerificationKeyResolverPort, VerificationKeyResult

class ProtectedEnvelopeIssuerBase(ProtectedEnvelopeIssuerPort, ABC):
    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope: raise NotImplementedError

class ProtectedEnvelopeVerifierBase(ProtectedEnvelopeVerifierPort, ABC):
    def verify(self, request: EnvelopeVerificationRequest, /) -> EnvelopeVerificationResult: raise NotImplementedError

class VerificationKeyResolverBase(VerificationKeyResolverPort, ABC):
    def resolve_verification_key(self, request: VerificationKeyRequest, /) -> VerificationKeyResult: raise NotImplementedError

__all__ = ["ProtectedEnvelopeIssuerBase", "ProtectedEnvelopeVerifierBase", "VerificationKeyResolverBase"]