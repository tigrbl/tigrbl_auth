from tigrbl_attestation_appraiser import ReferenceBackedAttestationAppraiser
from tigrbl_attestation_reference_provider import InMemoryReferenceMaterialProvider
from tigrbl_corim_store_provider import InMemoryCorimStore
from tigrbl_eat_verifier_provider import EatVerifierProvider
from tigrbl_identity_contracts.attestation import (
    AttestationEvidence,
    ReferenceIntegrityManifest,
)
from tigrbl_identity_contracts.tokens import (
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
            issuer_trust=IssuerTrustResult(
                self._trusted, "https://attester.example"
            ),
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


def test_eat_verifier_requires_both_valid_claims_and_integrity_provider():
    evidence = _evidence()
    assert not EatVerifierProvider().verify_evidence(evidence).trusted
    verifier = EatVerifierProvider(jwt_verifier=_TokenVerifier(evidence.claims))
    result = verifier.verify_evidence(evidence)
    assert result.verified
    assert result.evidence is not None
    assert result.evidence.envelope.envelope.format.value == "jwt"
    assert result.evidence.envelope.envelope.profile.value == "entity-attestation-token"
    assert not EatVerifierProvider(
        jwt_verifier=_TokenVerifier(evidence.claims, valid=False)
    ).verify_evidence(evidence).verified


def test_eat_verifier_rejects_wrong_profile_untrusted_issuer_and_replay():
    evidence = _evidence()
    assert not EatVerifierProvider(
        jwt_verifier=_TokenVerifier(
            evidence.claims, profile=TokenProfile.ACCESS_TOKEN
        )
    ).verify_evidence(evidence).verified
    assert not EatVerifierProvider(
        jwt_verifier=_TokenVerifier(evidence.claims, trusted=False)
    ).verify_evidence(evidence).verified
    assert not EatVerifierProvider(
        jwt_verifier=_TokenVerifier(evidence.claims),
        expected_issuer="https://other-attester.example",
    ).verify_evidence(evidence).verified
    assert not EatVerifierProvider(
        jwt_verifier=_TokenVerifier(evidence.claims, replay_accepted=False)
    ).verify_evidence(evidence).verified


def test_eat_verifier_uses_authenticated_claims_and_rejects_modified_claims():
    evidence = _evidence()
    modified = dict(evidence.claims)
    modified["measurement"] = "tampered"
    result = EatVerifierProvider(
        jwt_verifier=_TokenVerifier(evidence.claims)
    ).verify_evidence(AttestationEvidence(evidence.profile, modified, evidence.raw))
    assert not result.verified
    assert "authenticated token claims" in result.reason


def test_eat_verifier_selects_cwt_verifier_and_passes_trust_expectations():
    claims = {265: "urn:example:eat-profile", 10: b"12345678"}
    verifier = _TokenVerifier(claims)
    provider = EatVerifierProvider(
        cwt_verifier=verifier,
        expected_issuer="https://attester.example",
        expected_audience="https://verifier.example",
    )
    result = provider.verify_evidence(
        AttestationEvidence("urn:example:eat-profile", claims, b"cose-sign1")
    )

    assert result.verified
    assert result.evidence is not None
    assert result.evidence.envelope.envelope.format.value == "cwt"
    assert verifier.last_request.expected_issuer == "https://attester.example"
    assert verifier.last_request.expected_audience == "https://verifier.example"


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


def test_corim_store_validates_and_publishes_immutable_reference_material():
    store = InMemoryCorimStore()
    value = {
        "tag-identity": "corim-1",
        "tags": [
            {
                "tag-type": "comid",
                "tag-identity": "comid-1",
                "entities": [],
                "triples": {},
                "reference-values": {"measurement": "approved"},
            }
        ],
    }
    store.publish(value)
    assert store.resolve_manifest("corim-1").tag_identity == "corim-1"
    try:
        store.publish(value)
    except ValueError:
        pass
    else:
        raise AssertionError("immutable CoRIM was overwritten")
