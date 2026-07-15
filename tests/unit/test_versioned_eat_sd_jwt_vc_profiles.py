import pytest

from tigrbl_attestation_protocol_eat import (
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION as EAT_VERSION,
    EAT_CWT_CARRIER,
    EAT_JWT_CARRIER,
    UnsupportedEatCarrierError,
    capability_report as eat_capability_report,
    compatibility as eat_compatibility,
    migrate_claims as migrate_eat,
    select_carrier,
    supports as eat_supports,
)
from tigrbl_credential_profile_sd_jwt_vc import (
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


def test_eat_owns_rfc_9711_history_and_features() -> None:
    assert EAT_VERSION.identifier == "RFC9711"
    assert eat_supports("nested-tokens")
    assert migrate_eat(
        {"eat_profile": "urn:example:eat"}, source="draft-ietf-rats-eat-30"
    ) == {"eat_profile": "urn:example:eat"}
    with pytest.raises(ValueError, match="eat_profile"):
        migrate_eat({}, source="draft-ietf-rats-eat-30")


def test_eat_owns_carriers_compatibility_and_capability_bindings() -> None:
    assert select_carrier("application/eat+jwt") is EAT_JWT_CARRIER
    assert select_carrier("application/eat+cwt") is EAT_CWT_CARRIER
    with pytest.raises(UnsupportedEatCarrierError):
        select_carrier("application/jwt")

    path = eat_compatibility("draft-ietf-rats-eat-30")
    assert path.compatible and path.migration_required
    operations = {requirement.operation for requirement in CAPABILITY_REQUIREMENTS}
    assert operations == {
        "appraise",
        "record_result",
        "resolve_reference_material",
        "verify_evidence",
    }
    report = eat_capability_report()
    assert report["selected_revision"] == "RFC9711"
    assert report["required_capabilities"] == ("attestation.appraisal",)


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
