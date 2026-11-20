from typing import Protocol
from .envelopes import ProtectedEnvelope
from .keys import VerificationKeyRequest, VerificationKeyResult
from .operations import EnvelopeProtectionRequest, EnvelopeVerificationRequest, EnvelopeVerificationResult

class ProtectedEnvelopeIssuerPort(Protocol):
    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope: ...

class ProtectedEnvelopeVerifierPort(Protocol):
    def verify(self, request: EnvelopeVerificationRequest, /) -> EnvelopeVerificationResult: ...

class VerificationKeyResolverPort(Protocol):
    def resolve_verification_key(self, request: VerificationKeyRequest, /) -> VerificationKeyResult: ...