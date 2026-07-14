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
    TokenVerificationRequest,
    TokenVerifierPort,
    VerifiedTokenEnvelope,
)


class EatVerifierProvider(EvidenceVerifierBase):
    def __init__(
        self,
        *,
        jwt_verifier: TokenVerifierPort | None = None,
        cwt_verifier: TokenVerifierPort | None = None,
        expected_issuer: str | None = None,
        expected_audience: str | None = None,
    ):
        self._jwt_verifier = jwt_verifier
        self._cwt_verifier = cwt_verifier
        self._expected_issuer = expected_issuer
        self._expected_audience = expected_audience

    def verify_evidence(
        self, evidence: AttestationEvidence, /
    ) -> EvidenceVerificationResult:
        if evidence.raw is None:
            return EvidenceVerificationResult(False, "protected EAT token is required")
        if isinstance(evidence.raw, bytes):
            encoding = EatEncoding.CBOR
            envelope_format = TokenEnvelopeFormat.CWT
            verifier = self._cwt_verifier
        else:
            encoding = EatEncoding.JSON
            envelope_format = TokenEnvelopeFormat.JWT
            verifier = self._jwt_verifier
        if verifier is None:
            return EvidenceVerificationResult(
                False, f"no EAT {envelope_format.value.upper()} verifier configured"
            )
        envelope = ProtectedTokenEnvelope(
            evidence.raw,
            envelope_format,
            TokenProfile.ENTITY_ATTESTATION_TOKEN,
        )
        verification = verifier.verify(
            TokenVerificationRequest(
                token=evidence.raw,
                expected_profile=TokenProfile.ENTITY_ATTESTATION_TOKEN,
                expected_issuer=self._expected_issuer,
                expected_audience=self._expected_audience,
            )
        )
        if not verification.valid:
            reason = "; ".join(verification.errors) or "token verification failed"
            return EvidenceVerificationResult(False, f"EAT integrity verification failed: {reason}")
        if verification.profile != TokenProfile.ENTITY_ATTESTATION_TOKEN:
            return EvidenceVerificationResult(False, "verified token has the wrong profile")
        if verification.issuer_trust is None or not verification.issuer_trust.trusted:
            return EvidenceVerificationResult(False, "EAT issuer is not trusted")
        if (
            self._expected_issuer is not None
            and verification.issuer_trust.issuer != self._expected_issuer
        ):
            return EvidenceVerificationResult(
                False, "EAT issuer does not match the expected issuer"
            )
        if verification.replay is not None and not verification.replay.accepted:
            return EvidenceVerificationResult(False, "EAT freshness or replay validation failed")
        authenticated_claims = dict(verification.claims)
        try:
            parsed = parse_eat_claims(authenticated_claims, encoding)
            validate_eat_claims(parsed)
        except ValueError as exc:
            return EvidenceVerificationResult(False, f"invalid EAT claims: {exc}")
        if str(parsed.profile.identifier) != evidence.profile:
            return EvidenceVerificationResult(False, "EAT profile does not match evidence profile")
        if evidence.claims and dict(evidence.claims) != authenticated_claims:
            return EvidenceVerificationResult(
                False, "supplied EAT claims do not match authenticated token claims"
            )
        authenticated_evidence = AttestationEvidence(
            evidence.profile,
            authenticated_claims,
            evidence.raw,
        )
        verified_envelope = VerifiedTokenEnvelope(envelope, authenticated_claims)
        return EvidenceVerificationResult(
            True,
            "EAT claims and integrity verified",
            VerifiedAttestationEvidence(authenticated_evidence, verified_envelope),
            authenticated_claims,
        )


__all__ = ["EatVerifierProvider"]
