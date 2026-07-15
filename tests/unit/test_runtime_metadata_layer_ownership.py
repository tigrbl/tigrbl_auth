from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_runtime_capability_metadata_is_owned_by_layer_60_certification() -> None:
    old_owner = (
        ROOT
        / "pkgs/50-protocols/tigrbl-authz-resource-server/src"
        / "tigrbl_authz_resource_server/runtime_metadata.py"
    )
    canonical_owner = (
        ROOT
        / "pkgs/60-runtime/tigrbl-auth-release-certification/src"
        / "tigrbl_auth_release_certification/runtime_metadata.py"
    )

    assert not old_owner.exists()
    assert canonical_owner.exists()
    source = canonical_owner.read_text(encoding="utf-8")
    assert "runtime_truth_manifest" in source
    assert "build_capability_attestation" in source


def test_runtime_metadata_consumers_target_the_layer_60_owner() -> None:
    facade = (
        ROOT
        / "pkgs/70-facade/tigrbl-auth/src/tigrbl_auth/security/runtime_metadata.py"
    ).read_text(encoding="utf-8")
    server = (
        ROOT
        / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server"
        / "resource_validation_metadata_runtime.py"
    ).read_text(encoding="utf-8")

    target = "tigrbl_auth_release_certification.runtime_metadata"
    assert target in facade
    assert target in server
    assert "tigrbl_authz_resource_server.runtime_metadata" not in facade
    assert "tigrbl_authz_resource_server.runtime_metadata" not in server


def test_layer_50_resource_server_has_no_certification_runtime_dependency() -> None:
    resource_manifest = (
        ROOT / "pkgs/50-protocols/tigrbl-authz-resource-server/pyproject.toml"
    ).read_text(encoding="utf-8")
    certification_manifest = (
        ROOT / "pkgs/60-runtime/tigrbl-auth-release-certification/pyproject.toml"
    ).read_text(encoding="utf-8")

    assert "tigrbl-auth-release-certification" not in resource_manifest
    assert "tigrbl-identity-runtime" not in resource_manifest
    assert "tigrbl-identity-contracts" in certification_manifest


def test_resource_server_contract_module_is_a_runtime_neutral_compatibility_export() -> None:
    source = (
        ROOT
        / "pkgs/50-protocols/tigrbl-authz-resource-server/src"
        / "tigrbl_authz_resource_server/contracts.py"
    ).read_text(encoding="utf-8")

    assert "tigrbl_auth_protocol_oauth.standards.resource_verifier_contract" in source
    assert "tigrbl_identity_runtime" not in source
