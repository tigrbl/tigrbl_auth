from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment


ROOT = Path(__file__).resolve().parents[3]
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-api-public" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

from tigrbl_auth_api_public import PRODUCT_SURFACE, PUBLIC_API_CONTRACT, build_app


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        require_tls=False,
        admin_api_key="test-admin-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


def test_public_api_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(product_surface=PRODUCT_SURFACE)

    assert PRODUCT_SURFACE == "public-api"
    assert PUBLIC_API_CONTRACT.product_surface == PRODUCT_SURFACE
    assert PUBLIC_API_CONTRACT.intended_uix == "@tigrbl-auth/public-uix"
    assert deployment.plugin_mode == "public-only"
    assert deployment.surface_enabled("public-rest")
    assert not deployment.surface_enabled("admin-rpc")
    assert deployment.active_openrpc_methods == ()


def test_public_api_contract_routes_are_public_only() -> None:
    baseline = resolve_deployment(product_surface=PRODUCT_SURFACE)
    production = resolve_deployment(profile="production", product_surface=PRODUCT_SURFACE)

    for capability in PUBLIC_API_CONTRACT.baseline_capabilities:
        assert baseline.capability_enabled(capability), capability

    for capability in PUBLIC_API_CONTRACT.production_capabilities:
        assert production.capability_enabled(capability), capability

    for route in PUBLIC_API_CONTRACT.forbidden_exact_routes:
        assert route not in production.active_routes

    for prefix in PUBLIC_API_CONTRACT.forbidden_route_prefixes:
        assert all(
            not active_route.startswith(prefix)
            for active_route in production.active_routes
        )


@pytest.mark.asyncio
async def test_public_api_app_fails_closed_for_control_plane_paths(
    tmp_path: Path,
) -> None:
    public_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=public_app), base_url="http://test"
    ) as client:
        rpc = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        tenant = await client.get("/tenant")
        diagnostics = await client.get("/diagnostics")

    assert rpc.status_code == 404
    assert tenant.status_code == 404
    assert diagnostics.status_code == 404
