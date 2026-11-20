import pytest

from tba_profile_credential_sd_jwt_vc import (
    CAPABILITY_REQUIREMENTS as SD_JWT_VC_REQUIREMENTS,
    CURRENT_VERSION as SD_JWT_VC_VERSION,
    SD_JWT_VC_CARRIER,
    UnsupportedSdJwtVcMediaTypeError,
    capability_report as sd_jwt_vc_capability_report,
    compatibility as sd_jwt_vc_compatibility,
    migrate_claims as migrate_sd_jwt_vc,
    select_carrier as select_sd_jwt_vc_carrier,
    supports as sd_jwt_vc_supports,
)


def test_sd_jwt_vc_owns_draft_history_and_labels_draft_status() -> None:
    assert SD_JWT_VC_VERSION.identifier == "draft-17"
    assert SD_JWT_VC_VERSION.status == "active-draft"
    assert sd_jwt_vc_supports("dc-media-type")
    assert migrate_sd_jwt_vc({"vct": "urn:example:credential"}, source="draft-13") == {
        "vct": "urn:example:credential"
    }


def test_sd_jwt_vc_owns_carrier_compatibility_and_explicit_bindings() -> None:
    path = sd_jwt_vc_compatibility("draft-13")
    assert path.compatible and path.migration_required
    assert select_sd_jwt_vc_carrier("application/dc+sd-jwt") is SD_JWT_VC_CARRIER
    with pytest.raises(UnsupportedSdJwtVcMediaTypeError):
        select_sd_jwt_vc_carrier("application/vc+sd-jwt")

    assert {item.operation for item in SD_JWT_VC_REQUIREMENTS} == {
        "decode",
        "encode",
        "validate",
    }
    report = sd_jwt_vc_capability_report()
    assert report["required_capabilities"] == ("artifact.processing",)
