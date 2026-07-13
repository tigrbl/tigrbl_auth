from collections.abc import Callable

from tigrbl_attestation_bases import EvidenceVerifierBase
from tigrbl_eat_concrete import EatEncoding, parse_eat_claims, validate_eat_claims
from tigrbl_identity_contracts.attestation import AppraisalResult, AttestationEvidence

IntegrityVerifier = Callable[[bytes | str, str], bool]


class EatVerifierProvider(EvidenceVerifierBase):
    def __init__(self, integrity_verifier: IntegrityVerifier | None = None):
        self._integrity_verifier = integrity_verifier

    def verify_evidence(self, evidence: AttestationEvidence, /) -> AppraisalResult:
        encoding = (
            EatEncoding.CBOR
            if any(isinstance(name, int) for name in evidence.claims)
            else EatEncoding.JSON
        )
        try:
            parsed = parse_eat_claims(evidence.claims, encoding)
            validate_eat_claims(parsed)
        except ValueError as exc:
            return AppraisalResult(False, f"invalid EAT claims: {exc}")
        if str(parsed.profile.identifier) != evidence.profile:
            return AppraisalResult(False, "EAT profile does not match evidence profile")
        if evidence.raw is None:
            return AppraisalResult(False, "protected EAT token is required")
        if self._integrity_verifier is None:
            return AppraisalResult(False, "no EAT integrity verifier configured")
        if not self._integrity_verifier(evidence.raw, evidence.profile):
            return AppraisalResult(False, "EAT integrity verification failed")
        return AppraisalResult(
            True, "EAT claims and integrity verified", dict(evidence.claims)
        )


__all__ = ["EatVerifierProvider", "IntegrityVerifier"]
