import pytest

from tba_protocol_attestation_eat import (
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
