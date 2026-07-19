import json
from tigrbl_jwt_concrete import validate_registered_claims
from tigrbl_protected_envelope_contracts import (
    EnvelopeVerificationRequest,
    ProtectedEnvelope,
)


class JwtProtocol:
    def __init__(self, capability, profile):
        self.capability, self.profile = capability, profile

    def verify(
        self,
        envelope: ProtectedEnvelope,
        *,
        issuer: str | None = None,
        audience: str | None = None,
        now: int | None = None,
    ):
        result = self.capability.verify_envelope(
            EnvelopeVerificationRequest(
                envelope,
                expected_profile=self.profile.name,
                expected_issuer=issuer,
                expected_audience=audience,
            )
        )
        if not result.valid or result.payload is None:
            raise ValueError(result.reason or "JWT signature verification failed")
        claims = json.loads(result.payload)
        self.profile.validate(envelope.protected_headers, claims)
        validate_registered_claims(claims, issuer=issuer, audience=audience, now=now)
        return claims, result
