import pytest

from tigrbl_auth_profile_haip import (
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION,
    HAIP_PROOF_CLAIM_CLASSES,
    capability_report,
    compatibility,
    configure_haip,
    migrate_configuration,
    supports,
)


def test_haip_owns_final_profile_version_and_composed_features() -> None:
    assert CURRENT_VERSION.identifier == "1.0"
    assert CURRENT_VERSION.status == "final"
    assert supports("oid4vci-1.0")
    assert supports("oid4vp-1.0")
    assert supports("dcql")


def test_haip_accepts_only_profile_credential_formats() -> None:
    configuration = configure_haip(
        credential_formats=frozenset({"dc+sd-jwt", "mso_mdoc"})
    )
    assert configuration.wallet_attestation
    with pytest.raises(ValueError, match="unsupported HAIP credential formats"):
        configure_haip(credential_formats=frozenset({"jwt_vc_json"}))


def test_haip_refuses_lossy_draft_presentation_migration() -> None:
    with pytest.raises(ValueError, match="explicit DCQL migration"):
        migrate_configuration({"presentation_definition": {}}, source="draft-03")
    assert migrate_configuration({}, source="draft-03") == {
        "oid4vci_version": "1.0",
        "oid4vp_version": "1.0",
    }


def test_haip_composes_claim_families_and_required_capability_profile() -> None:
    path = compatibility("draft-03")
    assert path.compatible and path.migration_required and not path.lossless
    assert {claim.claim_name for claim in HAIP_PROOF_CLAIM_CLASSES} >= {
        "aud",
        "client_id",
        "iat",
        "nonce",
        "txn",
    }
    assert {item.operation for item in CAPABILITY_REQUIREMENTS} == {
        "check_and_reserve",
        "issue",
        "present",
        "validate",
        "verify_evidence",
        "verify_presentation",
        "verify_wallet_attestation",
    }
    report = capability_report()
    assert report["required_capabilities"] == (
        "artifact.processing",
        "attestation.appraisal",
        "digital-credential.issuance",
        "digital-credential.presentation",
        "security.replay-protection",
    )
