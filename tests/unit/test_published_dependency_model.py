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

    assert "tigrbl==0.4.4.dev1" in dependencies
    assert "tigrbl-core==0.4.4.dev1" in dependencies
    assert "swarmauri_core==0.10.0" in dependencies
    assert "swarmauri_standard==0.10.0" in dependencies
    assert "swarmauri_tokens_jwt==0.3.0.dev31" in dependencies
    assert "swarmauri_crypto_jwe==0.3.0.dev5" in dependencies
    assert "pqcrypto==0.4.0" not in dependencies
    assert "tigrbl-security-signing-pqc==0.1.0" in dependencies

    assert set({"postgres", "sqlite", "uvicorn", "hypercorn", "tigrcorn", "servers"}) <= set(extras)
    assert extras["uvicorn"] == ["uvicorn[standard]==0.41.0"]
    assert "sqlalchemy[asyncio]==2.0.49" in dependencies
    assert "pydantic[email]==2.12.5" in dependencies
    assert extras["hypercorn"] == ["hypercorn==0.18.0"]
    assert extras["tigrcorn"] == ["tigrcorn==0.3.8; python_version >= '3.11'"]
    assert "tigrcorn==0.3.8; python_version >= '3.11'" in extras["servers"]

    jose_dependencies = set(_load_package_pyproject("tigrbl-identity-jose")["project"]["dependencies"])
    facade_dependencies = set(_load_package_pyproject("tigrbl-auth")["project"]["dependencies"])
    pqc_provider_dependencies = set(_load_package_pyproject("tigrbl-security-signing-pqc")["project"]["dependencies"])
    decision_engine_dependencies = set(_load_package_pyproject("tigrbl-authz-policy-decision-engine")["project"]["dependencies"])
    invariant_registry_dependencies = set(_load_package_pyproject("tigrbl-authz-policy-invariant-registry")["project"]["dependencies"])
    rbac_administrator_dependencies = set(_load_package_pyproject("tigrbl-authz-policy-rbac-administrator")["project"]["dependencies"])
    service_identity_registry_dependencies = set(_load_package_pyproject("tigrbl-authz-policy-service-identity-registry")["project"]["dependencies"])
    authz_dependencies = set(_load_package_pyproject("tigrbl-authz-policy")["project"]["dependencies"])
    storage_dependencies = set(_load_package_pyproject("tigrbl-identity-storage")["project"]["dependencies"])
    assert "pqcrypto==0.4.0" not in jose_dependencies
    assert "tigrbl-security-signing-pqc==0.1.0" in jose_dependencies
    assert "pqcrypto==0.4.0" not in facade_dependencies
    assert "tigrbl-security-signing-pqc==0.1.0" in facade_dependencies
    assert "pqcrypto==0.4.0" in pqc_provider_dependencies
    assert "pqcrypto==0.4.0" not in decision_engine_dependencies
    assert "tigrbl-authz-policy-concrete==0.4.0.dev2" in decision_engine_dependencies
    assert "pqcrypto==0.4.0" not in invariant_registry_dependencies
    assert "tigrbl-identity-contracts==0.4.0.dev2" in invariant_registry_dependencies
    assert "pqcrypto==0.4.0" not in rbac_administrator_dependencies
    assert "tigrbl-identity-storage==0.4.0.dev2" in rbac_administrator_dependencies
    assert "pqcrypto==0.4.0" not in service_identity_registry_dependencies
    assert "tigrbl-identity-concrete==0.4.0.dev2" in service_identity_registry_dependencies
    assert "pqcrypto==0.4.0" not in authz_dependencies
    assert "tigrbl-authz-policy-decision-engine==0.4.0.dev2" in authz_dependencies
    assert "tigrbl-authz-policy-invariant-registry==0.4.0.dev2" in authz_dependencies
    assert "tigrbl-authz-policy-rbac-administrator==0.4.0.dev2" in authz_dependencies
    assert "tigrbl-authz-policy-service-identity-registry==0.4.0.dev2" in authz_dependencies
    assert "tigrbl-identity-storage==0.4.0.dev2" in authz_dependencies
    assert "tigrbl-authz-policy==0.4.0.dev2" not in storage_dependencies


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
        "constraints/runner-uvicorn.txt",
        "constraints/runner-hypercorn.txt",
        "constraints/runner-tigrcorn.txt",
        "docs/runbooks/INSTALLATION_PROFILES.md",
        "docs/runbooks/CLEAN_CHECKOUT_REPRO.md",
        ".github/workflows/ci-install-profiles.yml",
        "scripts/verify_clean_room_install_substrate.py",
        "scripts/run_certification_lane.py",
    }
    assert required <= set(_dependency_artifact_paths(ROOT))

    dockerfile = (ROOT / "docker" / "Dockerfile").read_text(encoding="utf-8")
    assert "./pkgs/" not in dockerfile
    assert "constraints/base.txt" not in dockerfile
    assert "constraints/runner-uvicorn.txt" in dockerfile


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
    assert isinstance(summary["migration_portability_passed"], bool)
    assert summary["base_dependency_count"] >= 12
    assert summary["base_exact_pinned_dependency_count"] == summary["base_dependency_count"]
