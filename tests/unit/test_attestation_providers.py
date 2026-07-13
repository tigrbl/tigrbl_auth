from tigrbl_attestation_appraiser import ReferenceBackedAttestationAppraiser
from tigrbl_attestation_reference_provider import InMemoryReferenceMaterialProvider
from tigrbl_corim_store_provider import InMemoryCorimStore
from tigrbl_eat_verifier_provider import EatVerifierProvider
from tigrbl_identity_contracts.attestation import (
    AttestationEvidence,
    ReferenceIntegrityManifest,
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
    verifier = EatVerifierProvider(lambda token, profile: token == "signed.eat.token")
    result = verifier.verify_evidence(evidence)
    assert result.verified
    assert result.evidence is not None
    assert result.evidence.envelope.envelope.format.value == "jwt"
    assert result.evidence.envelope.envelope.profile.value == "entity-attestation-token"
    assert not verifier.verify_evidence(
        AttestationEvidence(evidence.profile, evidence.claims, raw="bad")
    ).trusted


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
        EatVerifierProvider(lambda token, profile: True),
        references,
        {"urn:example:eat-profile": "reference-1"},
    )
    assert appraiser.appraise(_evidence()).trusted
    assert not appraiser.appraise(_evidence("tampered")).trusted


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
