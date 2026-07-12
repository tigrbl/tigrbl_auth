import pytest
from tigrbl_corim_concrete import (
    CORIM_REVISION,
    parse_corim,
    parse_corim_tag,
    validate_corim_tag,
)
from tigrbl_eat_concrete import (
    RFC_REVISION,
    EatEncoding,
    parse_detached_bundle,
    parse_eat,
    parse_eat_claims,
    validate_eat_claims,
)


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
    assert evidence.profile == "urn:example:eat-profile"
    assert RFC_REVISION == "RFC 9711"
    assert not hasattr(evidence, "identity")


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


def test_corim_family_models_reference_material_not_evidence():
    value = {
        "tag-identity": "corim-1",
        "signer": "manufacturer",
        "tags": [
            {
                "tag-type": "comid",
                "tag-identity": "comid-1",
                "entities": [{"name": "manufacturer"}],
                "triples": {"reference-triples": [{"measurement": "expected"}]},
            },
            {
                "tag-type": "coswid",
                "tag-id": "coswid-1",
                "software-name": "Firmware",
                "entity": [],
            },
        ],
    }
    tag = parse_corim_tag(value)
    validate_corim_tag(tag)
    manifest = parse_corim(value)
    assert len(manifest.manifests) == 2
    assert CORIM_REVISION == "draft-ietf-rats-corim-11"
    assert not hasattr(tag, "measured_state")


def test_corim_rejects_duplicate_embedded_tag_identities():
    tag = parse_corim_tag(
        {
            "tag-identity": "corim",
            "tags": [
                {
                    "tag-type": "comid",
                    "tag-identity": "same",
                    "entities": [],
                    "triples": {},
                },
                {
                    "tag-type": "comid",
                    "tag-identity": "same",
                    "entities": [],
                    "triples": {},
                },
            ],
        }
    )
    with pytest.raises(ValueError, match="unique"):
        validate_corim_tag(tag)
