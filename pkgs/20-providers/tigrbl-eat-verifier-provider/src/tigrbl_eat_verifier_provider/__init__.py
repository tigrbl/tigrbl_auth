from collections.abc import Callable

from tigrbl_attestation_bases import EvidenceVerifierBase
from tigrbl_eat_concrete import EatEncoding, parse_eat_claims, validate_eat_claims
from tigrbl_identity_contracts.attestation import (
    AttestationEvidence,
    EvidenceVerificationResult,
    VerifiedAttestationEvidence,
)
from tigrbl_identity_contracts.tokens import (
    ProtectedTokenEnvelope,
    TokenEnvelopeFormat,
    TokenProfile,
    VerifiedTokenEnvelope,
)

IntegrityVerifier = Callable[[bytes | str, str], bool]


class EatVerifierProvider(EvidenceVerifierBase):
    def __init__(self, integrity_verifier: IntegrityVerifier | None = None):
        self._integrity_verifier = integrity_verifier

    def verify_evidence(
        self, evidence: AttestationEvidence, /
    ) -> EvidenceVerificationResult:
        encoding = (
            EatEncoding.CBOR
            if any(isinstance(name, int) for name in evidence.claims)
            else EatEncoding.JSON
        )
        try:
            parsed = parse_eat_claims(evidence.claims, encoding)
            validate_eat_claims(parsed)
        except ValueError as exc:
            return EvidenceVerificationResult(False, f"invalid EAT claims: {exc}")
        if str(parsed.profile.identifier) != evidence.profile:
            return EvidenceVerificationResult(False, "EAT profile does not match evidence profile")
        if evidence.raw is None:
            return EvidenceVerificationResult(False, "protected EAT token is required")
        if self._integrity_verifier is None:
            return EvidenceVerificationResult(False, "no EAT integrity verifier configured")
        if not self._integrity_verifier(evidence.raw, evidence.profile):
            return EvidenceVerificationResult(False, "EAT integrity verification failed")
        envelope = ProtectedTokenEnvelope(
            evidence.raw,
            TokenEnvelopeFormat.CWT if encoding is EatEncoding.CBOR else TokenEnvelopeFormat.JWT,
            TokenProfile.ENTITY_ATTESTATION_TOKEN,
        )
        verified_envelope = VerifiedTokenEnvelope(envelope, dict(evidence.claims))
        return EvidenceVerificationResult(
            True,
            "EAT claims and integrity verified",
            VerifiedAttestationEvidence(evidence, verified_envelope),
            dict(evidence.claims),
        )


__all__ = ["EatVerifierProvider", "IntegrityVerifier"]
