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
        ROOT / "pkgs/70-facade/tigrbl-auth/src/tigrbl_auth/security/runtime_metadata.py"
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


def test_resource_server_contract_module_is_a_runtime_neutral_compatibility_export() -> (
    None
):
    source = (
        ROOT
        / "pkgs/50-protocols/tigrbl-authz-resource-server/src"
        / "tigrbl_authz_resource_server/contracts.py"
    ).read_text(encoding="utf-8")

    assert "tigrbl_auth_protocol_oauth.standards.resource_verifier_contract" in source
    assert "tigrbl_identity_runtime" not in source


def test_oauth_security_profiles_consume_injected_runtime_state() -> None:
    oauth_root = (
        ROOT
        / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src"
        / "tigrbl_auth_protocol_oauth"
    )
    manifest = (
        ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/pyproject.toml"
    ).read_text(encoding="utf-8")
    security_profile = (
        oauth_root / "standards/_rfc9700/security_profile.py"
    ).read_text(encoding="utf-8")
    verifier_contract = (
        oauth_root / "standards/resource_verifier_contract.py"
    ).read_text(encoding="utf-8")
    server_adapter = (
        ROOT
        / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server"
        / "introspection_surface.py"
    ).read_text(encoding="utf-8")

    assert "tigrbl-identity-runtime" not in manifest
    assert "tigrbl_identity_runtime" not in security_profile
    assert "tigrbl_identity_runtime" not in verifier_contract
    assert "deployment_from_request" in server_adapter
    assert "build_protected_resource_verifier_contract" in server_adapter


def test_oidc_discovery_projection_consumes_injected_runtime_state() -> None:
    oidc_root = (
        ROOT
        / "pkgs/50-protocols/tigrbl-auth-protocol-oidc/src"
        / "tigrbl_auth_protocol_oidc"
    )
    rp_client = (
        ROOT
        / "pkgs/50-protocols/tigrbl-auth-protocol-rp/src"
        / "tigrbl_auth_protocol_rp/discovery_client.py"
    ).read_text(encoding="utf-8")
    metadata = (oidc_root / "standards/discovery_metadata.py").read_text(
        encoding="utf-8"
    )
    owner = (oidc_root / "standards/discovery.py").read_text(encoding="utf-8")
    server_runtime = (
        ROOT
        / "pkgs/60-runtime/tigrbl-identity-server/src"
        / "tigrbl_identity_server/oidc_discovery_runtime.py"
    ).read_text(encoding="utf-8")
    facade = (
        ROOT / "pkgs/70-facade/tigrbl-auth/src/tigrbl_auth/oidc_discovery.py"
    ).read_text(encoding="utf-8")

    assert "class OidcDiscoveryDeployment(Protocol)" in metadata
    assert "def build_openid_config(deployment:" in metadata
    for source in (metadata, owner, rp_client):
        assert "tigrbl_identity_runtime" not in source
        assert "tigrbl_identity_storage_runtime" not in source
    assert "resolve_deployment" in server_runtime
    assert "tigrbl_identity_server.oidc_discovery_runtime" in facade


def test_discovery_artifact_operations_are_owned_by_the_cli_runtime() -> None:
    old_owner = (
        ROOT
        / "pkgs/50-protocols/tigrbl-auth-protocol-oidc/src"
        / "tigrbl_auth_protocol_oidc/discovery_service.py"
    )
    canonical_owner = (
        ROOT
        / "pkgs/60-runtime/tigrbl-identity-cli/src"
        / "tigrbl_identity_cli/discovery_service.py"
    )

    assert not old_owner.exists()
    assert canonical_owner.exists()
    source = canonical_owner.read_text(encoding="utf-8")
    for operation in (
        "show_discovery",
        "validate_discovery",
        "publish_discovery",
        "diff_discovery",
    ):
        assert f"def {operation}" in source


def test_oidc_logout_protocol_consumes_injected_durable_operations() -> None:
    oidc_root = (
        ROOT
        / "pkgs/50-protocols/tigrbl-auth-protocol-oidc/src"
        / "tigrbl_auth_protocol_oidc/standards"
    )
    protocol_sources = [
        (oidc_root / name).read_text(encoding="utf-8")
        for name in (
            "_rp_logout_validation.py",
            "backchannel_logout.py",
            "frontchannel_logout.py",
            "rp_initiated_logout.py",
        )
    ]
    for source in protocol_sources:
        assert "tigrbl_identity_runtime" not in source
        assert "tigrbl_identity_storage_runtime" not in source
    assert "registration_metadata: Mapping" in protocol_sources[1]
    assert "register_replay:" in protocol_sources[1]
    assert "registration_metadata: Mapping" in protocol_sources[2]
    assert "registration_resolver:" in protocol_sources[3]


def test_durable_oidc_logout_planning_is_owned_by_layer_60() -> None:
    server_runtime = (
        ROOT
        / "pkgs/60-runtime/tigrbl-identity-server/src"
        / "tigrbl_identity_server/logout_runtime.py"
    ).read_text(encoding="utf-8")
    rp_compatibility = (
        ROOT
        / "pkgs/50-protocols/tigrbl-auth-protocol-rp/src"
        / "tigrbl_auth_protocol_rp/logout.py"
    ).read_text(encoding="utf-8")

    assert "async def build_logout_plan(" in server_runtime
    assert "oidc_persistence" in server_runtime
    assert "build_frontchannel_descriptor" in server_runtime
    assert "build_backchannel_descriptor" in server_runtime
    assert "tigrbl_identity_runtime" not in rp_compatibility
    assert "tigrbl_identity_storage_runtime" not in rp_compatibility
    assert "build_logout_plan" not in rp_compatibility


def test_oidc_session_protocol_is_runtime_and_storage_neutral() -> None:
    oidc_package = ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oidc"
    session_protocol = (
        oidc_package
        / "src/tigrbl_auth_protocol_oidc/standards/session_mgmt.py"
    ).read_text(encoding="utf-8")
    manifest = (oidc_package / "pyproject.toml").read_text(encoding="utf-8")
    handler_runtime = (
        ROOT
        / "pkgs/60-runtime/tigrbl-identity-server/src"
        / "tigrbl_identity_server/security/handler_records.py"
    ).read_text(encoding="utf-8")

    assert "tigrbl_identity_runtime" not in session_protocol
    assert "tigrbl_identity_storage_runtime" not in session_protocol
    assert "resolve_browser_session" not in session_protocol
    assert "create_browser_session" not in session_protocol
    assert "tigrbl-identity-runtime" not in manifest
    assert "tigrbl-identity-storage" not in manifest
    assert "resolve_browser_session_record" in handler_runtime
    assert "create_browser_session_record" in handler_runtime
