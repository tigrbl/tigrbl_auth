from __future__ import annotations

from tigrbl_authz_resource_server import (
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION,
    RESOURCE_SERVER_ACCESS_TOKEN_CLAIM_CLASSES,
    SPECIFICATION_VERSIONS,
    build_protected_resource_authorization_capability,
    capability_report,
    compatibility,
    migrate_verifier_metadata,
    supports,
)
from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_confirmation_concrete import ConfirmationClaim
from tigrbl_claim_expiration_concrete import ExpirationClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_scope_concrete import ScopeClaim
from tigrbl_claim_subject_concrete import SubjectClaim


def test_resource_server_profile_catalogs_peer_rfc_versions() -> None:
    assert CURRENT_VERSION.identifier == "tigrbl-oauth-protected-resource-1.0"
    assert CURRENT_VERSION.status == "implementation-profile"
    assert {item.identifier for item in SPECIFICATION_VERSIONS} == {
        "RFC6750",
        "RFC7662",
        "RFC8705",
        "RFC9068",
        "RFC9449",
        "RFC9700",
        "RFC9728",
    }
    assert supports("fail-closed")
    assert supports("dpop-sender-constraint")


def test_resource_server_profile_exposes_explicit_legacy_migration() -> None:
    path = compatibility("legacy-unversioned")
    assert path.compatible and path.lossless and path.migration_required
    metadata = {"issuer": "https://issuer.example", "fail_closed": True}
    assert (
        migrate_verifier_metadata(
            metadata,
            source="legacy-unversioned",
        )
        == metadata
    )


def test_resource_server_profile_composes_standalone_access_token_claims() -> None:
    claim_classes = set(RESOURCE_SERVER_ACCESS_TOKEN_CLAIM_CLASSES)
    assert {
        IssuerClaim,
        SubjectClaim,
        AudienceClaim,
        ExpirationClaim,
        ScopeClaim,
        ConfirmationClaim,
    } <= claim_classes


def test_resource_server_profile_maps_rfc_obligations_to_capabilities() -> None:
    report = capability_report()
    assert report["requirements"] == CAPABILITY_REQUIREMENTS
    assert set(report["required_capabilities"]) == {
        "artifact.processing",
        "policy.evaluation",
        "protected-resource.authorization",
        "security.replay-protection",
        "token.introspection",
    }
    assert {item.revision for item in CAPABILITY_REQUIREMENTS} == {
        "RFC6750",
        "RFC7662",
        "RFC8705",
        "RFC9068",
        "RFC9449",
        "RFC9700",
        "RFC9728",
    }


def test_resource_server_profile_builds_reportable_authorization_capability() -> None:
    capability = build_protected_resource_authorization_capability()
    report = capability.capability_report()
    assert report["capability_id"] == "protected-resource.authorization"
    assert report["operations"] == ("verify_token", "verify_claims")
