from tigrbl_attestation_protocol_corim import (
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION,
    VERSION_HISTORY,
    capability_report,
    migrate_document,
    supports,
)


def test_corim_protocol_owns_version_history_features_and_upgrade_path() -> None:
    assert CURRENT_VERSION.identifier == "draft-ietf-rats-corim-11"
    assert len(VERSION_HISTORY) >= 2
    assert supports(CURRENT_VERSION.identifier, "cots")
    assert migrate_document(
        {"tag-identity": "tag-1"},
        from_version="draft-ietf-rats-corim-10",
        to_version=CURRENT_VERSION.identifier,
    )["profile"] == "tag:ietf.org,2025:corim"


def test_corim_protocol_maps_wire_requirements_to_normalized_capabilities() -> None:
    report = capability_report()
    assert report["selected_revision"] == CURRENT_VERSION.identifier
    assert set(CAPABILITY_REQUIREMENTS).issubset(set(report["requirements"]))
    assert {item.capability_id for item in CAPABILITY_REQUIREMENTS} == {
        "attestation.reference-material",
        "attestation.appraisal",
    }
    assert "unsupported" not in report
