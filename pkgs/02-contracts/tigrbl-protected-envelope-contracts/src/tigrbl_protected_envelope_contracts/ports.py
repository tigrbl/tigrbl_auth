"""Protected-envelope extension ports."""

from typing import Protocol

from .envelopes import ProtectedEnvelope
from .operations import EnvelopeProtectionRequest, EnvelopeVerificationRequest, EnvelopeVerificationResult


class ProtectedEnvelopeIssuerPort(Protocol):
    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope: ...


class ProtectedEnvelopeVerifierPort(Protocol):
    def verify(self, request: EnvelopeVerificationRequest, /) -> EnvelopeVerificationResult: ...


__all__ = ["ProtectedEnvelopeIssuerPort", "ProtectedEnvelopeVerifierPort"]