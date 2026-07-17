from __future__ import annotations

import sys
from inspect import signature
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.config.deployment import DEFAULT_VALUES


ROOT = Path(__file__).resolve().parents[3]
PKG_SRC = ROOT / "pkgs" / "80-routers" / "tigrbl-auth-backend-app-platform-admin" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

build_app = import_module("tigrbl_auth_backend_app_platform_admin").build_app
admin_tenants = import_module("tigrbl_auth_backend_app_platform_admin.tenants")


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8015",
        protected_resource_identifier="http://localhost:8015/resource",
        require_tls=False,
        admin_api_key="test-platform-admin-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


@pytest.mark.asyncio
async def test_platform_admin_realm_routes_are_admin_only(tmp_path: Path) -> None:
    platform_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=platform_app), base_url="http://test"
    ) as client:
        missing_key = await client.get("/admin/realm")
        raw_realm = await client.get(
            "/realm", headers={"X-API-Key": "test-platform-admin-key"}
        )
        openapi = await client.get("/openapi.json")

    assert missing_key.status_code == 401
    assert missing_key.json()["error"] == "missing_admin_api_key"
    assert raw_realm.status_code == 404
    paths = openapi.json()["paths"]
    assert "/admin/realm" in paths
    assert set(paths["/admin/realm"]) == {"get", "post"}
    assert set(paths["/admin/realm/{realm_id}"]) == {"get", "patch", "delete"}
    assert set(paths["/admin/realm/{realm_id}/tenant"]) == {"get", "post"}


def test_platform_admin_tenant_handlers_use_create_and_update_contracts() -> None:
    create_payload = signature(admin_tenants.admin_create_tenant).parameters["payload"]
    update_payload = signature(admin_tenants.admin_update_tenant).parameters["payload"]

    assert "AdminTenantProvisionIn" in str(create_payload.annotation)
    assert "AdminTenantUpdateIn" in str(update_payload.annotation)
