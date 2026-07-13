import pytest

from tigrbl_auth_profile_haip import (
    CURRENT_VERSION,
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
