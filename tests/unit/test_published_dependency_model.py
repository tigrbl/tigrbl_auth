from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib
from pathlib import Path
from types import SimpleNamespace

from tigrbl_auth.cli.reports import _dependency_artifact_paths, generate_state_reports


ROOT = Path(__file__).resolve().parents[2]


def _load_pyproject() -> dict:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def _load_package_pyproject(name: str) -> dict:
    matches = sorted((ROOT / "pkgs").glob(f"**/{name}/pyproject.toml"))
    assert matches, name
    return tomllib.loads(matches[0].read_text(encoding="utf-8"))


def test_pyproject_uses_published_pins_and_extras():
    manifest = _load_pyproject()
    project = manifest["project"]
    dependencies = set(project["dependencies"])
    extras = project["optional-dependencies"]
    removed_helper_pins = {
        "tigrbl-authz-policy-abac-administrator==0.4.0.dev2",
        "tigrbl-authz-policy-delegated-administrator==0.4.0.dev2",
        "tigrbl-authz-policy-engine==0.4.0.dev2",
        "tigrbl-authz-policy-rbac-administrator==0.4.0.dev2",
        "tigrbl-authz-policy-service-identity-registry==0.4.0.dev2",
        "tigrbl-authz-resource-server-dpop-cnf-binding-validator==0.4.0.dev2",
        "tigrbl-authz-resource-server-introspection-client==0.4.0.dev2",
        "tigrbl-authz-resource-server-jwks-cache==0.4.0.dev2",
        "tigrbl-authz-resource-server-mtls-cnf-binding-validator==0.4.0.dev2",
        "tigrbl-authz-resource-server-sender-constraint-validator==0.4.0.dev2",
    }

    assert "tigrbl==0.4.4.dev1" in dependencies
    assert "tigrbl-core==0.4.4.dev1" in dependencies
    assert "swarmauri_core==0.10.0" in dependencies
    assert "swarmauri_standard==0.10.0" in dependencies
    assert "swarmauri_tokens_jwt==0.3.0.dev31" in dependencies
    assert "swarmauri_crypto_jwe==0.3.0.dev5" in dependencies
    assert "pqcrypto==0.4.0" not in dependencies
    assert "tigrbl-security-signing-pqc==0.1.0" in dependencies
    assert "tigrbl-authz-resource-server-verifier==0.4.0.dev2" in dependencies
    assert "tigrbl-security-token-verification==0.4.0.dev2" not in dependencies
    assert "tigrbl-security-token-jwks-cache==0.1.0" in dependencies
    assert "tigrbl-security-token-introspection-client==0.1.0" in dependencies
    assert "tigrbl-security-sender-constraint-validator==0.1.0" in dependencies
    assert "tigrbl-authz-policy-concrete==0.4.0.dev2" not in dependencies
    assert "tigrbl-identity-concrete==0.4.0.dev2" not in dependencies
    assert "tigrbl-authz-policy-rules-concrete==0.4.0.dev2" in dependencies
    assert "tigrbl-identity-identities-concrete==0.4.0.dev2" in dependencies
    assert "tigrbl-identity-credentials-concrete==0.4.0.dev2" in dependencies
    assert "tigrbl-security-authorization-provenance-builder==0.1.0" in dependencies
    assert dependencies.isdisjoint(removed_helper_pins)

    assert set({"postgres", "sqlite", "uvicorn", "hypercorn", "tigrcorn", "servers"}) <= set(extras)
    assert extras["uvicorn"] == ["tigrbl-identity-runtime[uvicorn]==0.4.0.dev2"]
    assert "sqlalchemy[asyncio]==2.0.49" in dependencies
    assert "pydantic[email]==2.12.5" in dependencies
    assert extras["hypercorn"] == ["tigrbl-identity-runtime[hypercorn]==0.4.0.dev2"]
    assert extras["tigrcorn"] == ["tigrbl-identity-runtime[tigrcorn]==0.4.0.dev2"]
    assert extras["servers"] == ["tigrbl-identity-runtime[servers]==0.4.0.dev2"]

    runtime_extras = _load_package_pyproject("tigrbl-identity-runtime")["project"]["optional-dependencies"]
    assert runtime_extras["uvicorn"] == ["uvicorn[standard]==0.41.0"]
    assert runtime_extras["hypercorn"] == ["hypercorn==0.18.0"]
    assert runtime_extras["tigrcorn"] == ["tigrcorn==0.3.8; python_version >= '3.11'"]
    assert "tigrcorn==0.3.8; python_version >= '3.11'" in runtime_extras["servers"]

    jose_dependencies = set(_load_package_pyproject("tigrbl-identity-jose")["project"]["dependencies"])
    oidc_dependencies = set(_load_package_pyproject("tigrbl-auth-protocol-oidc")["project"]["dependencies"])
    facade_dependencies = set(_load_package_pyproject("tigrbl-auth")["project"]["dependencies"])
    pqc_provider_dependencies = set(_load_package_pyproject("tigrbl-security-signing-pqc")["project"]["dependencies"])
    admin_gate_dependencies = set(_load_package_pyproject("tigrbl-authz-policy-admin-gate")["project"]["dependencies"])
    authz_rules_dependencies = set(
        _load_package_pyproject("tigrbl-authz-policy-rules-concrete")["project"]["dependencies"]
    )
    identity_credentials_dependencies = set(
        _load_package_pyproject("tigrbl-identity-credentials-concrete")["project"]["dependencies"]
    )
    identity_identities_dependencies = set(
        _load_package_pyproject("tigrbl-identity-identities-concrete")["project"]["dependencies"]
    )
    identity_admin_dependencies = set(_load_package_pyproject("tigrbl-identity-admin")["project"]["dependencies"])
    authority_graph_dependencies = set(
        _load_package_pyproject("tigrbl-authz-policy-authority-derivation-graph")["project"]["dependencies"]
    )
    trust_graph_dependencies = set(
        _load_package_pyproject("tigrbl-identity-admin-trust-federation-graph")["project"]["dependencies"]
    )
    authz_dependencies = set(_load_package_pyproject("tigrbl-authz-policy")["project"]["dependencies"])
    verifier_dependencies = set(_load_package_pyproject("tigrbl-authz-resource-server-verifier")["project"]["dependencies"])
    jwks_cache_dependencies = set(_load_package_pyproject("tigrbl-security-token-jwks-cache")["project"]["dependencies"])
    introspection_dependencies = set(_load_package_pyproject("tigrbl-security-token-introspection-client")["project"]["dependencies"])
    sender_constraint_dependencies = set(_load_package_pyproject("tigrbl-security-sender-constraint-validator")["project"]["dependencies"])
    resource_server_dependencies = set(_load_package_pyproject("tigrbl-authz-resource-server")["project"]["dependencies"])
    storage_dependencies = set(_load_package_pyproject("tigrbl-identity-storage")["project"]["dependencies"])
    storage_runtime_dependencies = set(
        _load_package_pyproject("tigrbl-identity-storage-runtime")["project"][
            "dependencies"
        ]
    )
    operator_dependencies = set(_load_package_pyproject("tigrbl-identity-operator")["project"]["dependencies"])
    deprecated_policy_dependencies = set(_load_package_pyproject("tigrbl-identity-policy")["project"]["dependencies"])

    assert "pqcrypto==0.4.0" not in jose_dependencies
    assert "tigrbl-security-signing-pqc==0.1.0" in jose_dependencies
    assert "tigrbl-auth-protocol-oidc-backchannel-replay-store==0.4.0.dev2" not in oidc_dependencies
    assert "tigrbl-identity-storage==0.4.0.dev2" in oidc_dependencies
    assert "tigrbl-identity-concrete==0.4.0.dev2" not in oidc_dependencies
    assert oidc_dependencies.isdisjoint(removed_helper_pins)
    assert "pqcrypto==0.4.0" not in facade_dependencies
    assert "tigrbl-security-signing-pqc==0.1.0" in facade_dependencies
    assert "tigrbl-authz-policy-authority-derivation-graph==0.4.0.dev2" in facade_dependencies
    assert "tigrbl-authz-policy-concrete==0.4.0.dev2" not in facade_dependencies
    assert "tigrbl-authz-policy-rules-concrete==0.4.0.dev2" in facade_dependencies
    assert "tigrbl-authz-policy-invariant-registry==0.4.0.dev2" in facade_dependencies
    assert facade_dependencies.isdisjoint(removed_helper_pins)
    assert "pqcrypto==0.4.0" in pqc_provider_dependencies
    assert "pqcrypto==0.4.0" not in admin_gate_dependencies
    assert "tigrbl-identity-core==0.4.0.dev2" in admin_gate_dependencies
    assert "tigrbl-identity-runtime==0.4.0.dev2" in admin_gate_dependencies
    assert "pqcrypto==0.4.0" not in authz_rules_dependencies
    assert "tigrbl-identity-contracts==0.4.0.dev2" in authz_rules_dependencies
    assert "tigrbl-identity-core==0.4.0.dev2" not in authz_rules_dependencies
    assert "pqcrypto==0.4.0" not in identity_credentials_dependencies
    assert "pqcrypto==0.4.0" not in identity_identities_dependencies
    assert "tigrbl-identity-contracts==0.4.0.dev2" in identity_credentials_dependencies
    assert "tigrbl-identity-contracts==0.4.0.dev2" in identity_identities_dependencies
    assert "tigrbl-identity-core==0.4.0.dev2" not in identity_credentials_dependencies
    assert "tigrbl-identity-jose==0.4.0.dev2" not in identity_credentials_dependencies
    assert "tigrbl-identity-admin-control-plane==0.4.0.dev2" in identity_admin_dependencies
    assert "tigrbl-identity-admin-advanced-authenticator-registry==0.4.0.dev2" not in identity_admin_dependencies
    assert "tigrbl-identity-admin-policy-registry==0.4.0.dev2" not in identity_admin_dependencies
    assert "tigrbl-identity-admin-federation-registry==0.4.0.dev2" not in identity_admin_dependencies
    assert "tigrbl-identity-storage==0.4.0.dev2" in authority_graph_dependencies
    assert "tigrbl-identity-storage==0.4.0.dev2" in trust_graph_dependencies
    assert "tigrbl-identity-admin-relationship-graph==0.4.0.dev2" in identity_admin_dependencies
    assert "tigrbl-identity-jose==0.4.0.dev2" in identity_admin_dependencies
    assert "tigrbl-identity-concrete==0.4.0.dev2" not in identity_admin_dependencies
    assert "tigrbl-identity-identities-concrete==0.4.0.dev2" in identity_admin_dependencies
    assert "tigrbl-identity-credentials-concrete==0.4.0.dev2" in identity_admin_dependencies
    assert identity_admin_dependencies.isdisjoint(removed_helper_pins)
    assert "pqcrypto==0.4.0" not in authz_dependencies
    assert "tigrbl-authz-policy-concrete==0.4.0.dev2" not in authz_dependencies
    assert "tigrbl-authz-policy-rules-concrete==0.4.0.dev2" in authz_dependencies
    assert "tigrbl-identity-storage==0.4.0.dev2" in authz_dependencies
    assert authz_dependencies.isdisjoint(removed_helper_pins)
    assert "tigrbl-authz-policy==0.4.0.dev2" not in storage_dependencies
    assert "tigrbl-auth-protocol-oauth==0.4.0.dev2" in storage_runtime_dependencies
    assert "tigrbl-auth-protocol-oidc==0.4.0.dev2" in storage_runtime_dependencies
    assert "tigrbl-authz-resource-server==0.4.0.dev2" in storage_runtime_dependencies
    assert "pqcrypto==0.4.0" not in verifier_dependencies
    assert "tigrbl-identity-contracts==0.4.0.dev2" in verifier_dependencies
    assert "tigrbl-security-token-jwks-cache==0.1.0" in verifier_dependencies
    assert "tigrbl-security-token-introspection-client==0.1.0" in verifier_dependencies
    assert "tigrbl-authz-resource-server==0.4.0.dev2" not in verifier_dependencies
    assert "tigrbl-security-trust-domain-bases==0.1.0" in jwks_cache_dependencies
    assert "tigrbl-security-trust-domain-bases==0.1.0" in introspection_dependencies
    assert "tigrbl-security-dpop-cnf-binding-validator==0.1.0" in sender_constraint_dependencies
    assert "tigrbl-security-mtls-cnf-binding-validator==0.1.0" in sender_constraint_dependencies
    assert "tigrbl-security-token-verification==0.4.0.dev2" not in resource_server_dependencies
    assert "tigrbl-authz-resource-server-verifier==0.4.0.dev2" in resource_server_dependencies
    assert "tigrbl-security-sender-constraint-validator==0.1.0" in resource_server_dependencies
    assert resource_server_dependencies.isdisjoint(removed_helper_pins)
    assert "tigrbl-authz-policy==0.4.0.dev2" in operator_dependencies
    assert "tigrbl-authz-policy-concrete==0.4.0.dev2" not in operator_dependencies
    assert operator_dependencies.isdisjoint(removed_helper_pins)
    assert "tigrbl-authz-policy==0.4.0.dev2" in deprecated_policy_dependencies
    assert "tigrbl-authz-policy-invariant-registry==0.4.0.dev2" in deprecated_policy_dependencies
    assert "tigrbl-authz-policy-concrete==0.4.0.dev2" not in deprecated_policy_dependencies
    assert deprecated_policy_dependencies.isdisjoint(removed_helper_pins)


def test_tigrbl_router_uses_upstream_tigrbl_router():
    import tigrbl

    assert tigrbl.TigrblRouter is not None


def test_tigrbl_router_exposes_upstream_include_tables():
    import tigrbl

    assert callable(getattr(tigrbl.TigrblRouter, "include_tables", None))


def test_deployment_from_options_uses_active_settings_values():
    from tigrbl_auth.cli.artifacts import deployment_from_options

    deployment = deployment_from_options(
        settings_obj=SimpleNamespace(
            issuer="http://localhost:8001",
            protected_resource_identifier="http://localhost:8001/resource",
        ),
        profile="production",
    )

    assert deployment.issuer == "http://localhost:8001"
    assert deployment.protected_resource_identifier == "http://localhost:8001/resource"


def test_workspace_sources_removed_and_provenance_artifacts_exist():
    manifest = _load_pyproject()
    sources = manifest.get("tool", {}).get("uv", {}).get("sources", {})
    assert sources
    for source in sources.values():
        source_path = Path(source["path"])
        assert not source_path.is_absolute()
        assert ".." not in source_path.parts
        assert source_path.parts[0] == "pkgs"
        assert (ROOT / source_path / "pyproject.toml").is_file()

    required = {
        "docker/Dockerfile",
        "uv.lock",
        "pkgs/60-runtime/tigrbl-identity-runtime/pyproject.toml",
        "docs/runbooks/INSTALLATION_PROFILES.md",
        "docs/runbooks/CLEAN_CHECKOUT_REPRO.md",
        ".github/workflows/ci-install-profiles.yml",
        "scripts/verify_clean_room_install_substrate.py",
        "scripts/run_certification_lane.py",
    }
    assert required <= set(_dependency_artifact_paths(ROOT))

    dockerfile = (ROOT / "docker" / "Dockerfile").read_text(encoding="utf-8")
    assert "./pkgs/" not in dockerfile
    assert "\n    -c " not in dockerfile
    assert '".[sqlite,uvicorn]"' in dockerfile


def test_docker_assets_are_not_published_from_repository_root():
    root_docker_files = [
        path.name
        for path in ROOT.iterdir()
        if path.is_file()
        and (
            path.name == ".dockerignore"
            or path.name.startswith("Dockerfile")
            or path.name.startswith("docker-compose")
            or path.name.startswith("compose.")
        )
    ]

    assert root_docker_files == []

    docker_dir = ROOT / "docker"
    expected = {
        ".dockerignore",
        "Dockerfile",
        "Dockerfile.local-tigrbl",
        "Dockerfile.dev-tigrbl",
        "Dockerfile.dev-public-api",
        "Dockerfile.dev-resource-validation-api",
        "Dockerfile.dev-platform-admin-api",
        "Dockerfile.dev-tenant-admin-api",
        "Dockerfile.dev-developer-api",
        "Dockerfile.dev-my-account-api",
        "Dockerfile.dev-service-admin-api",
        "docker-compose.yml",
        "docker-compose.public-api.yml",
        "docker-compose.resource-validation-api.yml",
        "docker-compose.platform-admin-api.yml",
        "docker-compose.tenant-admin-api.yml",
        "docker-compose.developer-api.yml",
        "docker-compose.my-account-api.yml",
        "docker-compose.service-admin-api.yml",
        "docker-compose.demo-hub-uix.yml",
    }
    assert expected <= {path.name for path in docker_dir.iterdir()}

    root_context_dockerfiles = {
        "Dockerfile",
        "Dockerfile.local-tigrbl",
        "Dockerfile.dev-tigrbl",
        "Dockerfile.dev-public-api",
        "Dockerfile.dev-resource-validation-api",
        "Dockerfile.dev-platform-admin-api",
        "Dockerfile.dev-tenant-admin-api",
        "Dockerfile.dev-developer-api",
        "Dockerfile.dev-my-account-api",
        "Dockerfile.dev-service-admin-api",
    }
    for dockerfile in root_context_dockerfiles:
        assert (docker_dir / f"{dockerfile}.dockerignore").is_file()

    assert (
        ROOT / "pkgs" / "95-ui" / "demo-hub-uix" / "Dockerfile.dockerignore"
    ).is_file()


def test_state_report_tracks_dependency_model_checkpoint():
    payload = generate_state_reports(ROOT)
    summary = payload["current_state"]

    assert summary["workspace_sources_present"] is False
    assert summary["workspace_sources_declared"] is True
    assert summary["first_party_workspace_source_count"] > 0
    assert summary["forbidden_workspace_source_count"] == 0
    assert summary["dependency_source"] == "pyproject.toml"
    assert summary["native_uv_lock_present"] is True
    assert summary["install_profile_workflow_present"] is True
    assert summary["tigrcorn_extra_placeholder"] is False
    assert summary["tigrcorn_pin_committed"] is True
    assert summary["runtime_profile_placeholder_supported_runner_count"] == 0
    assert summary["runtime_profile_declared_ci_install_probe_complete"] is True
    assert summary["install_substrate_report_present"] is True
    assert summary["install_substrate_manifest_passed"] is True
    assert summary["install_substrate_tox_pip_check_complete"] is True
    assert summary["install_substrate_tox_import_probe_complete"] is True
    assert summary["test_extra_present"] is True
    assert isinstance(summary["migration_portability_passed"], bool)
    assert summary["base_dependency_count"] >= 12
    assert summary["base_exact_pinned_dependency_count"] == summary["base_dependency_count"]
