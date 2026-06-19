from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.cli.artifacts import (
    build_openapi_contract,
    deployment_from_options,
)
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.config.surfaces import (
    public_contract_paths,
    route_registry,
    surface_baseline_boundary_integrity,
    surface_baseline_boundary_manifest,
    surface_registry,
)


ROOT = Path(__file__).resolve().parents[2]

BOUNDARY_FEATURE_IDS = {
    "feat:uix-admin-boundary",
    "feat:uix-public-boundary",
    "feat:surface-applicability-classification",
    "feat:api-admin-boundary",
    "feat:api-admin-contract-publication-boundary",
    "feat:api-admin-authz-gate",
    "feat:api-admin-resource-management-boundary",
    "feat:api-admin-policy-control-plane-boundary",
    "feat:api-admin-public-surface-exclusion",
    "feat:api-public-boundary",
    "feat:api-public-oauth-boundary",
    "feat:api-public-oidc-boundary",
    "feat:api-public-discovery-boundary",
    "feat:api-public-registration-boundary",
    "feat:api-public-logout-boundary",
    "feat:api-public-admin-surface-exclusion",
}


def _settings(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(admin_api_key="test-admin-key", admin_api_key_dir=str(tmp_path))


def test_surface_baseline_boundary_t0_inventory_classifies_all_admin_public_api_and_uix_surfaces():
    manifest = surface_baseline_boundary_manifest()
    registry = surface_registry()
    admin_uix_pkg = json.loads((ROOT / "pkgs/90-ui/admin-uix/package.json").read_text())
    public_uix_pkg = json.loads((ROOT / "pkgs/90-ui/public-uix/package.json").read_text())

    assert set(manifest) == BOUNDARY_FEATURE_IDS
    assert registry["admin_control_plane"]["surface_set"] == "admin-rest"
    assert registry["public_auth_plane"]["surface_set"] == "public-rest"
    assert manifest["feat:uix-admin-boundary"]["audience"] == "admin"
    assert manifest["feat:uix-public-boundary"]["audience"] == "public"
    assert admin_uix_pkg["name"] == "@tigrbl-auth/admin-uix"
    assert public_uix_pkg["name"] == "@tigrbl-auth/public-uix"
    assert "/register" in public_contract_paths()
    assert "/logout" in public_contract_paths()


def test_surface_baseline_boundary_t1_composes_public_and_admin_contracts_by_profile():
    public_deployment = deployment_from_options(profile="production")
    mixed_deployment = deployment_from_options(profile="baseline", plugin_mode="mixed")
    public_openapi = build_openapi_contract(public_deployment, version="0.0.0-test")
    routes = route_registry()

    assert public_deployment.surface_enabled("public-rest")
    assert not public_deployment.surface_enabled("admin-rest")
    assert mixed_deployment.surface_enabled("public-rest")
    assert mixed_deployment.surface_enabled("admin-rest")
    assert "/authorize" in public_openapi["paths"]
    assert "/token" in public_openapi["paths"]
    assert "/.well-known/openid-configuration" in public_openapi["paths"]
    assert "/register" in public_openapi["paths"]
    assert "/logout" in public_openapi["paths"]
    assert "/rpc" not in public_openapi["paths"]
    assert {meta["surface_set"] for meta in routes.values()} <= {"public-rest", "diagnostics"}


@pytest.mark.asyncio
async def test_surface_baseline_boundary_t2_fails_closed_for_surface_leaks_and_admin_gate(tmp_path):
    integrity = surface_baseline_boundary_integrity()
    public_app = build_app(_settings(tmp_path), deployment=resolve_deployment())
    mixed_app = build_app(_settings(tmp_path), deployment=resolve_deployment(plugin_mode="mixed"))

    async with AsyncClient(transport=ASGITransport(app=public_app), base_url="http://test") as client:
        discovery = await client.get("/.well-known/openid-configuration")
        public_rpc = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        public_tenant = await client.get("/tenant")

    async with AsyncClient(transport=ASGITransport(app=mixed_app), base_url="http://test") as client:
        missing_admin_key = await client.get("/tenant")
        invalid_admin_key = await client.get("/tenant", headers={"X-API-Key": "wrong"})

    assert integrity["passed"] is True
    assert integrity["public_admin_leaks"] == []
    assert integrity["public_contract_leaks"] == []
    assert discovery.status_code == 200
    assert public_rpc.status_code == 404
    assert public_tenant.status_code == 404
    assert missing_admin_key.status_code == 404
    assert invalid_admin_key.status_code == 404
