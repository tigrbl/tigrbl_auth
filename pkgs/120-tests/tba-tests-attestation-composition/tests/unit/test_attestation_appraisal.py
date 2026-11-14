from tba_provider_attestation_appraiser import ReferenceBackedAttestationAppraiser
from tba_provider_attestation_reference import InMemoryReferenceMaterialProvider
from tba_provider_eat_verifier import EatVerifierProvider
from tba_contracts_identity.attestation import (
    AttestationEvidence,
    ReferenceIntegrityManifest,
)
from tba_contracts_identity.tokens import (
    IssuerTrustResult,
    ReplayValidation,
    TokenProfile,
    TokenVerificationResult,
)


class _TokenVerifier:
    def __init__(
        self,
        claims,
        *,
        valid: bool = True,
        profile: TokenProfile = TokenProfile.ENTITY_ATTESTATION_TOKEN,
        trusted: bool = True,
        replay_accepted: bool = True,
    ):
        self._claims = dict(claims)
        self._valid = valid
        self._profile = profile
        self._trusted = trusted
        self._replay_accepted = replay_accepted
        self.last_request = None

    def verify(self, request):
        self.last_request = request
        return TokenVerificationResult(
            valid=self._valid,
            profile=self._profile,
            claims=self._claims,
            errors=() if self._valid else ("invalid signature",),
            issuer_trust=IssuerTrustResult(self._trusted, "https://attester.example"),
            replay=ReplayValidation(self._replay_accepted, "eat-1"),
        )


def _evidence(measurement: str = "approved"):
    return AttestationEvidence(
        "urn:example:eat-profile",
        {
            "eat_profile": "urn:example:eat-profile",
            "eat_nonce": "12345678",
            "measurement": measurement,
        },
        raw="signed.eat.token",
    )


def test_reference_provider_is_explicit_and_rejects_duplicate_publication():
    provider = InMemoryReferenceMaterialProvider()
    manifest = ReferenceIntegrityManifest(
        "reference-1",
        ({"reference-values": {"measurement": "approved"}},),
        "manufacturer",
    )
    provider.publish(manifest)
    assert provider.resolve_manifest("reference-1") is manifest
    try:
        provider.publish(manifest)
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate reference manifest was accepted")


def test_appraiser_requires_verified_evidence_and_matching_reference_values():
    references = InMemoryReferenceMaterialProvider()
    references.publish(
        ReferenceIntegrityManifest(
            "reference-1",
            ({"reference-values": {"measurement": "approved"}},),
        )
    )
    appraiser = ReferenceBackedAttestationAppraiser(
        references,
        {"urn:example:eat-profile": "reference-1"},
    )
    try:
        appraiser.appraise(_evidence())
    except TypeError as exc:
        assert "verified attestation evidence" in str(exc)
    else:
        raise AssertionError("raw evidence was accepted for appraisal")
    approved = _evidence()
    approved_result = EatVerifierProvider(
        jwt_verifier=_TokenVerifier(approved.claims)
    ).verify_evidence(approved)
    assert approved_result.evidence is not None
    assert appraiser.appraise(approved_result.evidence).trusted

    tampered = _evidence("tampered")
    tampered_result = EatVerifierProvider(
        jwt_verifier=_TokenVerifier(tampered.claims)
    ).verify_evidence(tampered)
    assert tampered_result.evidence is not None
    assert not appraiser.appraise(tampered_result.evidence).trusted
