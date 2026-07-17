from __future__ import annotations

import pytest

from tigrbl_security_protocol_jose import (
    CLAIMS_ARE_PROFILE_OWNED,
    CURRENT_VERSION,
    JOSE_CLAIM_CLASSES,
    VERSION_HISTORY,
    JoseArtifactKind,
    UnsupportedJoseMediaTypeError,
    capability_report,
    compatibility,
    migrate_configuration,
    select_carrier,
    select_version,
    supports,
)


def test_jose_suite_version_and_feature_history() -> None:
    assert select_version().identifier == "jose-suite-2020-bcp"
    assert select_version(VERSION_HISTORY[0].identifier) is VERSION_HISTORY[0]
    assert supports("jwt-bcp")
    assert not supports("jwt-bcp", "jose-suite-2015")

    with pytest.raises(ValueError, match="unsupported JOSE suite revision"):
        select_version("unknown")


def test_jose_compatibility_and_configuration_migration() -> None:
    path = compatibility("jose-suite-2015")
    assert path.compatible
    assert path.migration_required

    migrated = migrate_configuration({}, source="jose-suite-2015")
    assert migrated == {
        "require_explicit_algorithm_allowlist": True,
        "reject_unsafe_jwt_types": True,
    }
    assert migrate_configuration(
        {"custom": True},
        source=CURRENT_VERSION.identifier,
    ) == {"custom": True}


def test_jose_carriers_and_claim_ownership_boundary() -> None:
    assert select_carrier("application/jose").artifact_kind is JoseArtifactKind.JOSE
    assert select_carrier("application/jwk-set+json").artifact_kind is JoseArtifactKind.JWKS
    assert CLAIMS_ARE_PROFILE_OWNED
    assert JOSE_CLAIM_CLASSES == ()

    with pytest.raises(UnsupportedJoseMediaTypeError):
        select_carrier("application/json")


def test_jose_capability_report_projects_bound_operations() -> None:
    report = capability_report()

    assert report["protocol"] == "jose"
    assert report["selected_revision"] == CURRENT_VERSION.identifier
    requirements = {
        (item.capability_id, item.operation)
        for item in report["requirements"]
    }
    assert ("artifact.protection", "sign") in requirements
    assert ("artifact.protection", "verify") in requirements
    assert ("artifact.protection", "encrypt") in requirements
    assert ("artifact.protection", "decrypt") in requirements
