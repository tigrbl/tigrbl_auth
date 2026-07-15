import pytest

from tigrbl_auth_protocol_oauth import (
    CURRENT_VERSION as OAUTH_VERSION,
    migrate_client,
    supports as oauth_supports,
)
from tigrbl_auth_protocol_oidc import (
    CAPABILITY_REQUIREMENTS as OIDC_CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION as OIDC_VERSION,
    capability_report as oidc_capability_report,
    compatibility as oidc_compatibility,
    migrate_client_metadata,
    supports as oidc_supports,
)


def test_oauth_distinguishes_rfc_6749_from_oauth_21_draft_profile() -> None:
    assert OAUTH_VERSION.status == "active-draft-profile"
    assert oauth_supports("pkce-required")
    assert oauth_supports("implicit", "RFC6749")
    with pytest.raises(ValueError, match="removed grants"):
        migrate_client({"grant_types": ["implicit"]}, source="RFC6749")
    assert (
        migrate_client({"grant_types": ["authorization_code"]}, source="RFC6749")[
            "require_pkce"
        ]
        is True
    )


def test_oidc_owns_core_errata_history() -> None:
    assert OIDC_VERSION.identifier == "1.0-errata2"
    assert oidc_supports("errata-set-2")
    assert migrate_client_metadata({"subject_type": "pairwise"}, source="1.0") == {
        "subject_type": "pairwise"
    }
    path = oidc_compatibility("1.0")
    assert path.compatible and path.migration_required


def test_oidc_maps_explicit_id_token_and_logout_operations() -> None:
    assert {item.operation for item in OIDC_CAPABILITY_REQUIREMENTS} == {
        "check_and_reserve",
        "decode",
        "validate",
    }
    report = oidc_capability_report()
    assert report["required_capabilities"] == (
        "artifact.processing",
        "security.replay-protection",
    )
    assert {item.requirement_id for item in report["requirements"]} == {
        "logout-token-jti-replay",
        "oidc-id-token-decode",
        "oidc-id-token-validation",
    }
