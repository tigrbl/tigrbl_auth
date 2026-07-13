import pytest

from tigrbl_attestation_protocol_eat import (
    CURRENT_VERSION as EAT_VERSION,
    migrate_claims as migrate_eat,
    supports as eat_supports,
)
from tigrbl_credential_profile_sd_jwt_vc import (
    CURRENT_VERSION as SD_JWT_VC_VERSION,
    migrate_claims as migrate_sd_jwt_vc,
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


def test_sd_jwt_vc_owns_draft_history_and_labels_draft_status() -> None:
    assert SD_JWT_VC_VERSION.identifier == "draft-17"
    assert SD_JWT_VC_VERSION.status == "active-draft"
    assert sd_jwt_vc_supports("dc-media-type")
    assert migrate_sd_jwt_vc({"vct": "urn:example:credential"}, source="draft-13") == {
        "vct": "urn:example:credential"
    }
