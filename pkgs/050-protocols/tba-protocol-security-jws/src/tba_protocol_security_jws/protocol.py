from tba_primitives_identity import ProtectedEnvelopeKind
from tba_contracts_protected_envelope import (
    EnvelopeProtectionRequest,
    EnvelopeVerificationRequest,
    ProtectedEnvelope,
)


class JwsProtocol:
    def __init__(self, capability, profile):
        self.capability, self.profile = capability, profile

    def sign(
        self, payload: bytes, *, key_reference: str, headers: dict[str, object]
    ) -> ProtectedEnvelope:
        self.profile.validate_headers(headers)
        return self.capability.protect_envelope(
            EnvelopeProtectionRequest(
                ProtectedEnvelopeKind.JWS,
                payload,
                headers,
                key_reference,
                self.profile.name,
            )
        )

    def verify(
        self, envelope: ProtectedEnvelope, *, detached_payload: bytes | None = None
    ):
        self.profile.validate_headers(envelope.protected_headers)
        result = self.capability.verify_envelope(
            EnvelopeVerificationRequest(envelope, detached_payload, self.profile.name)
        )
        if not result.valid:
            raise ValueError(result.reason or "JWS verification failed")
        return result
