from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_identity_operator import OperatorWorkflow  # noqa: E402
from tigrbl_identity_runtime import (  # noqa: E402
    ReadinessStatus,
    provider_runtime_profile,
    readiness_diagnostic,
    resolve_config,
    resolve_feature_flags,
    testkit_provider_runtime_profile as build_testkit_provider_runtime_profile,
)
from tigrbl_identity_server import (  # noqa: E402
    SurfacePlane,
    assert_public_admin_separation,
    build_route_surface_registry,
    compose_server_manifest,
    provider_server_profile,
)


@pytest.mark.unit
def test_server_runtime_operator_t0_public_surfaces_are_importable() -> None:
    registry = build_route_surface_registry()
    manifest = compose_server_manifest(provider_server_profile())
    profile = provider_runtime_profile()
    workflow = OperatorWorkflow()

    assert "authorize" in registry
    assert "admin-principals" in manifest.route_names()
    assert profile.server_profile == "provider"
    assert workflow.export_state() == '{"jwks":{},"services":{},"tenants":{}}'


@pytest.mark.unit
def test_server_t1_manifest_registry_profile_and_surface_separation() -> None:
    profile = provider_server_profile()
    manifest = compose_server_manifest(profile)

    assert_public_admin_separation(manifest)

    assert {route.plane for route in manifest.public_routes} == {SurfacePlane.PUBLIC}
    assert {route.plane for route in manifest.admin_routes} == {SurfacePlane.ADMIN}
    assert "token" in manifest.route_names()
    assert "rpc" not in manifest.route_names()


@pytest.mark.unit
def test_runtime_t1_profiles_config_precedence_feature_flags_and_readiness() -> None:
    provider = provider_runtime_profile()
    testkit = build_testkit_provider_runtime_profile()
    config = resolve_config(
        defaults={"issuer": "https://default", "tenant": "default"},
        profile={"issuer": "https://profile"},
        environment={"tenant": "env"},
        explicit={"issuer": "https://explicit"},
    )
    flags = resolve_feature_flags(
        defaults={"surface_admin_enabled": False, "surface_public_enabled": True},
        profile=provider.feature_flags,
        explicit={"surface_admin_enabled": True},
    )
    ready = readiness_diagnostic(provider, {"storage": True, "routes": True, "keys": True})
    failed = readiness_diagnostic(provider, {"storage": True, "routes": False}, error="route registry failed")

    assert provider.name == "provider-runtime"
    assert testkit.feature_flags["seed_test_tenant"] is True
    assert config == {"issuer": "https://explicit", "tenant": "env"}
    assert flags["surface_admin_enabled"] is True
    assert ready.status == ReadinessStatus.READY
    assert failed.ready is False
    assert failed.error == "route registry failed"


@pytest.mark.unit
def test_operator_t1_bootstrap_release_evidence_and_import_export_roundtrip() -> None:
    workflow = OperatorWorkflow()
    tenant = workflow.bootstrap_tenant(
        tenant_id="tenant-a",
        issuer="https://issuer.example.test/tenant-a",
        display_name="Tenant A",
    )
    jwks = workflow.bootstrap_jwks(tenant_id=tenant.tenant_id, kids=("kid-b", "kid-a", "kid-a"))
    service = workflow.bootstrap_service_identity(
        tenant_id=tenant.tenant_id,
        service_id="svc-worker",
        scopes=("jobs.write", "jobs.read"),
    )
    evidence = workflow.package_release_evidence(
        package="tigrbl-identity-server",
        version="0.4.0.dev2",
        artifact_paths=("dist/tigrbl_identity_server.whl",),
    )
    imported = OperatorWorkflow.import_state(workflow.export_state())

    assert jwks.kids == ("kid-a", "kid-b")
    assert service.scopes == ("jobs.read", "jobs.write")
    assert evidence.package == "tigrbl-identity-server"
    assert imported.state == workflow.state


@pytest.mark.unit
def test_server_runtime_operator_t2_fail_closed_guards() -> None:
    workflow = OperatorWorkflow()

    with pytest.raises(ValueError, match="tenant bootstrap"):
        workflow.bootstrap_jwks(tenant_id="missing", kids=("kid-a",))
    with pytest.raises(ValueError, match="unsupported runner"):
        type(provider_runtime_profile())(name="bad", server_profile="provider", runner="twisted")

    failed = readiness_diagnostic(provider_runtime_profile(), {"storage": False})
    assert failed.status == ReadinessStatus.NOT_READY


@pytest.mark.unit
def test_server_runtime_operator_t2_import_boundaries() -> None:
    server_files = [
        Path("pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/__init__.py"),
        Path("pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/assembly.py"),
    ]
    runtime_files = [
        Path("pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/assembly.py"),
    ]
    operator_files = [
        Path("pkgs/60-runtime/tigrbl-identity-operator/src/tigrbl_identity_operator/workflows.py"),
    ]

    def imports_for(files: list[Path]) -> set[str]:
        imports: set[str] = set()
        for file in files:
            tree = ast.parse(file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                    imports.add(node.module.split(".")[0])
        return imports

    assert "tigrbl_identity_operator" not in imports_for(server_files)
    assert "tigrbl_auth" not in imports_for(server_files + runtime_files + operator_files)
    assert "tigrbl_identity_server" not in imports_for(operator_files)
