"""Protocol-neutral protected-envelope extension bases."""

from abc import ABC

from tigrbl_protected_envelope_contracts import (
    EnvelopeProtectionRequest,
    EnvelopeVerificationRequest,
    EnvelopeVerificationResult,
    ProtectedEnvelope,
    ProtectedEnvelopeIssuerPort,
    ProtectedEnvelopeVerifierPort,
)


class ProtectedEnvelopeIssuerBase(ProtectedEnvelopeIssuerPort, ABC):
    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope:
        raise NotImplementedError


class ProtectedEnvelopeVerifierBase(ProtectedEnvelopeVerifierPort, ABC):
    def verify(
        self,
        request: EnvelopeVerificationRequest,
        /,
    ) -> EnvelopeVerificationResult:
        raise NotImplementedError


__all__ = ["ProtectedEnvelopeIssuerBase", "ProtectedEnvelopeVerifierBase"]