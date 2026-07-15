import pytest

from tigrbl_auth_protocol_oauth import (
    CAPABILITY_REQUIREMENTS as OAUTH_CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION as OAUTH_VERSION,
    EXTENSION_SPECIFICATIONS,
    capability_report as oauth_capability_report,
    compatibility as oauth_compatibility,
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
    assert OAUTH_VERSION.identifier == "draft-ietf-oauth-v2-1-15"
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


def test_oauth_tracks_framework_history_separately_from_extension_rfcs() -> None:
    path = oauth_compatibility("RFC6749")
    assert path.compatible and path.migration_required and not path.lossless
    assert oauth_compatibility(OAUTH_VERSION.identifier).lossless

    extensions = {spec.identifier for spec in EXTENSION_SPECIFICATIONS}
    assert {
        "RFC7009",
        "RFC7662",
        "RFC8693",
        "RFC8705",
        "RFC9068",
        "RFC9126",
        "RFC9449",
        "RFC9700",
        "RFC9728",
    } <= extensions


def test_oauth_reports_reviewed_capability_bindings_without_generated_defaults() -> (
    None
):
    report = oauth_capability_report()
    assert report["selected_revision"] == OAUTH_VERSION.identifier
    assert report["requirements"] == OAUTH_CAPABILITY_REQUIREMENTS
    assert {item.capability_id for item in OAUTH_CAPABILITY_REQUIREMENTS} == set(
        report["required_capabilities"]
    )
    assert all(
        not item.requirement_id.startswith("oauth:") for item in report["requirements"]
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
