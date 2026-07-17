from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth_backend_app_core.surfaces import admin_resource_path_prefixes
from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment


ROOT = Path(__file__).resolve().parents[3]
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-backend-app-tenant-admin" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

tenant_admin_package = import_module("tigrbl_auth_backend_app_tenant_admin")
PRODUCT_SURFACE = tenant_admin_package.PRODUCT_SURFACE
TENANT_ADMIN_BACKEND_APP_CONTRACT = tenant_admin_package.TENANT_ADMIN_BACKEND_APP_CONTRACT
build_app = tenant_admin_package.build_app


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8016",
        protected_resource_identifier="http://localhost:8016/resource",
        require_tls=False,
        admin_api_key="test-tenant-admin-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


def test_tenant_admin_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert PRODUCT_SURFACE == "tenant-admin-app"
    assert TENANT_ADMIN_BACKEND_APP_CONTRACT.product_surface == PRODUCT_SURFACE
    assert TENANT_ADMIN_BACKEND_APP_CONTRACT.intended_uix == (
        "@tigrbl-auth/tenant-admin-uix"
    )
    assert deployment.plugin_mode == "admin-only"
    assert deployment.surface_enabled("admin-rest")
    assert not deployment.surface_enabled("public-rest")
    assert tuple(deployment.allowed_admin_resources) == (
        TENANT_ADMIN_BACKEND_APP_CONTRACT.admin_resources
    )
    assert tuple(deployment.allowed_admin_rest_groups) == (
        TENANT_ADMIN_BACKEND_APP_CONTRACT.admin_rest_groups
    )


def test_tenant_admin_build_app_uses_environment_backed_default_settings() -> None:
    with patch.dict(
        "os.environ",
        {
            "AUTHN_ISSUER": "http://localhost:8016",
            "TIGRBL_AUTH_PROFILE": "production",
            "TIGRBL_AUTH_REQUIRE_TLS": "false",
            "TIGRBL_AUTH_ADMIN_API_KEY": "env-tenant-admin-key",
        },
    ):
        built = build_app()

    assert built.deployment.issuer == "http://localhost:8016"
    assert built.deployment.product_surface == PRODUCT_SURFACE
    assert built.settings_obj.admin_api_key == "env-tenant-admin-key"
    assert built.settings_obj.require_tls is False


def test_tenant_admin_contract_routes_are_tenant_scoped_only() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    prefixes = admin_resource_path_prefixes(deployment)
    assert "/user" in prefixes
    assert "/client" in prefixes
    assert "/clientregistration" in prefixes
    assert "/consent" in prefixes
    assert "/authsession" not in prefixes
    assert "/tenant" not in prefixes
    assert "/service" not in prefixes

    for route in TENANT_ADMIN_BACKEND_APP_CONTRACT.forbidden_exact_routes:
        assert route not in deployment.active_routes


@pytest.mark.asyncio
async def test_tenant_admin_openapi_is_surface_constrained_and_openrpc_is_absent(
    tmp_path: Path,
) -> None:
    tenant_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=tenant_app), base_url="http://test"
    ) as client:
        openapi_response = await client.get("/openapi.json")
        openrpc_response = await client.get("/openrpc.json")

    assert openapi_response.status_code == 200
    assert openrpc_response.status_code == 404
    paths = openapi_response.json()["paths"]
    assert "/user" in paths
    assert "/client" in paths
    assert "/clientregistration" in paths
    assert "/consent" in paths
    assert "/authsession" not in paths
    assert "/tenant" not in paths
    assert "/service" not in paths
    for route in TENANT_ADMIN_BACKEND_APP_CONTRACT.forbidden_exact_routes:
        assert route not in paths


@pytest.mark.asyncio
async def test_tenant_admin_cors_allows_uix_origin_on_error_responses(
    tmp_path: Path,
) -> None:
    tenant_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=tenant_app), base_url="http://test"
    ) as client:
        preflight = await client.options(
            "/admin/auth/login",
            headers={
                "origin": "http://localhost:3012",
                "access-control-request-method": "POST",
                "access-control-request-headers": "content-type",
            },
        )
        anonymous = await client.get(
            "/user",
            headers={"origin": "http://localhost:3012"},
        )

    assert preflight.status_code == 204
    assert preflight.headers["access-control-allow-origin"] == "http://localhost:3012"
    assert preflight.headers["access-control-allow-credentials"] == "true"
    assert "content-type" in preflight.headers["access-control-allow-headers"]
    assert anonymous.status_code == 401
    assert anonymous.headers["access-control-allow-origin"] == "http://localhost:3012"
    assert anonymous.headers["access-control-allow-credentials"] == "true"


@pytest.mark.asyncio
async def test_tenant_admin_rpc_endpoint_is_not_supported(
    tmp_path: Path,
) -> None:
    tenant_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=tenant_app), base_url="http://test"
    ) as client:
        missing_key = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        login = await client.post("/login", json={})
        register = await client.post("/register", json={})
        token = await client.post("/token", data={})

    assert missing_key.status_code == 404
    assert login.status_code == 404
    assert register.status_code == 404
    assert token.status_code == 404


@pytest.mark.asyncio
async def test_tenant_admin_rpc_dispatch_is_absent(
    tmp_path: Path,
) -> None:
    tenant_app = build_app(_settings(tmp_path))
    headers = {"X-API-Key": "test-tenant-admin-key"}

    async with AsyncClient(
        transport=ASGITransport(app=tenant_app), base_url="http://test"
    ) as client:
        discover = await client.post(
            "/rpc",
            headers=headers,
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        platform_method = await client.post(
            "/rpc",
            headers=headers,
            json={"jsonrpc": "2.0", "method": "tenant.list", "params": {}, "id": 2},
        )
        service_method = await client.post(
            "/rpc",
            headers=headers,
            json={"jsonrpc": "2.0", "method": "token.inspect", "params": {}, "id": 3},
        )

    assert discover.status_code == 404
    assert platform_method.status_code == 404
    assert service_method.status_code == 404


@pytest.mark.asyncio
async def test_tenant_admin_rest_control_plane_requires_admin_key(
    tmp_path: Path,
) -> None:
    tenant_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=tenant_app), base_url="http://test"
    ) as client:
        missing_key = await client.get("/user")
        invalid_key = await client.get(
            "/user", headers={"X-API-Key": "wrong-tenant-admin-key"}
        )
        tenant = await client.get(
            "/tenant", headers={"X-API-Key": "test-tenant-admin-key"}
        )
        service = await client.get(
            "/service", headers={"X-API-Key": "test-tenant-admin-key"}
        )
        login = await client.post("/login", json={})

    assert missing_key.status_code == 401
    assert missing_key.json()["error"] == "missing_admin_api_key"
    assert invalid_key.status_code == 403
    assert invalid_key.json()["error"] == "invalid_admin_api_key"
    assert tenant.status_code == 404
    assert service.status_code == 404
    assert login.status_code == 404
