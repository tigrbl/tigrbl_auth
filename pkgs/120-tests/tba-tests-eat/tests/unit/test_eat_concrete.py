import pytest
from tba_concrete_eat import (
    RFC_REVISION,
    EatEncoding,
    parse_detached_bundle,
    parse_eat,
    parse_eat_claims,
    validate_eat_claims,
)
from tba_contracts_identity.attestation import AttestationEvidence


def test_eat_is_attestation_evidence_not_identity_or_authentication_token():
    claims = parse_eat_claims(
        {
            "eat_profile": "urn:example:eat-profile",
            "eat_nonce": "12345678",
            "ueid": "device-identifier",
            "iat": 10,
        },
        EatEncoding.JSON,
    )
    validate_eat_claims(claims)
    evidence = parse_eat(claims.raw_claims)
    assert isinstance(evidence, AttestationEvidence)
    assert evidence.profile == "urn:example:eat-profile"
    assert RFC_REVISION == "RFC 9711"
    assert not hasattr(evidence, "identity")


def test_eat_evidence_keeps_claims_envelope_and_appraisal_distinct():
    evidence = parse_eat(
        {"eat_profile": "urn:profile", "eat_nonce": "12345678"},
        protected_token="header.payload.signature",
    )
    assert evidence.claims["eat_profile"] == "urn:profile"
    assert evidence.raw == "header.payload.signature"
    assert not hasattr(evidence, "trusted")


def test_eat_nonce_encoding_and_size_rules_are_distinct():
    with pytest.raises(ValueError, match="CBOR EAT nonce"):
        validate_eat_claims(
            parse_eat_claims({265: "urn:profile", 10: b"short"}, EatEncoding.CBOR)
        )
    with pytest.raises(ValueError, match="JSON EAT nonce"):
        validate_eat_claims(
            parse_eat_claims(
                {"eat_profile": "urn:profile", "eat_nonce": "short"}, EatEncoding.JSON
            )
        )


def test_eat_submodules_and_detached_bundle_support_composite_entities():
    claims = parse_eat_claims(
        {"eat_profile": "urn:profile", "submods": {"tee": {"ueid": "subsystem"}}},
        EatEncoding.JSON,
    )
    bundle = parse_detached_bundle(
        {
            "detached_claim_sets": {"boot": {"measurement": "abc"}},
            "integrity_token": "a.b.c",
        }
    )
    assert claims.submodules[0].name == "tee" and "boot" in bundle.detached_claim_sets
