import pytest

from tigrbl_attestation_protocol_corim import (
    CAPABILITY_REQUIREMENTS,
    CORIM_CLAIM_CLASSES,
    CORIM_UNSIGNED_CARRIER,
    CURRENT_VERSION,
    UnsupportedCorimMediaTypeError,
    VERSION_HISTORY,
    capability_report,
    compatibility,
    migrate_document,
    select_carrier,
    supports,
)


def test_corim_protocol_owns_version_history_features_and_upgrade_path() -> None:
    assert CURRENT_VERSION.identifier == "draft-ietf-rats-corim-11"
    assert len(VERSION_HISTORY) >= 2
    assert supports(CURRENT_VERSION.identifier, "cots")
    assert (
        migrate_document(
            {"tag-identity": "tag-1"},
            from_version="draft-ietf-rats-corim-10",
            to_version=CURRENT_VERSION.identifier,
        )["profile"]
        == "tag:ietf.org,2025:corim"
    )


def test_corim_protocol_maps_wire_requirements_to_normalized_capabilities() -> None:
    report = capability_report()
    assert report["selected_revision"] == CURRENT_VERSION.identifier
    assert set(CAPABILITY_REQUIREMENTS).issubset(set(report["requirements"]))
    assert {item.capability_id for item in CAPABILITY_REQUIREMENTS} == {
        "artifact.processing",
        "attestation.appraisal",
    }
    assert {item.operation for item in CAPABILITY_REQUIREMENTS} == {
        "appraise",
        "decode",
        "encode",
        "resolve_reference_material",
        "validate",
    }
    assert "unsupported" not in report


def test_corim_distinguishes_reference_maps_from_claims_and_evidence() -> None:
    assert CORIM_CLAIM_CLASSES == ()
    path = compatibility("draft-ietf-rats-corim-10")
    assert path.compatible and path.migration_required
    assert select_carrier("application/corim-unsigned+cbor") is CORIM_UNSIGNED_CARRIER
    with pytest.raises(UnsupportedCorimMediaTypeError):
        select_carrier("application/eat+cwt")
