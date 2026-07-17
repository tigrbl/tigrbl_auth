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
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-backend-app-developer" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

developer_package = import_module("tigrbl_auth_backend_app_developer")
PRODUCT_SURFACE = developer_package.PRODUCT_SURFACE
DEVELOPER_BACKEND_APP_CONTRACT = developer_package.DEVELOPER_BACKEND_APP_CONTRACT
build_app = developer_package.build_app


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8017",
        protected_resource_identifier="http://localhost:8017/resource",
        require_tls=False,
        admin_api_key="test-developer-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


def test_developer_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert PRODUCT_SURFACE == "developer-app"
    assert DEVELOPER_BACKEND_APP_CONTRACT.product_surface == PRODUCT_SURFACE
    assert DEVELOPER_BACKEND_APP_CONTRACT.intended_uix == "@tigrbl-auth/developer-uix"
    assert deployment.plugin_mode == "mixed"
    assert deployment.surface_enabled("public-rest")
    assert deployment.surface_enabled("admin-rest")
    assert tuple(deployment.active_capabilities) == (
        DEVELOPER_BACKEND_APP_CONTRACT.public_capabilities
    )
    assert tuple(deployment.allowed_admin_resources) == (
        DEVELOPER_BACKEND_APP_CONTRACT.admin_resources
    )
    assert tuple(deployment.allowed_admin_rest_groups) == (
        DEVELOPER_BACKEND_APP_CONTRACT.admin_rest_groups
    )


def test_developer_build_app_uses_environment_backed_default_settings() -> None:
    with patch.dict(
        "os.environ",
        {
            "AUTHN_ISSUER": "http://localhost:8017",
            "TIGRBL_AUTH_PROFILE": "production",
            "TIGRBL_AUTH_REQUIRE_TLS": "false",
            "TIGRBL_AUTH_ADMIN_API_KEY": "env-developer-key",
        },
    ):
        built = build_app()

    assert built.deployment.issuer == "http://localhost:8017"
    assert built.deployment.product_surface == PRODUCT_SURFACE
    assert built.settings_obj.admin_api_key == "env-developer-key"
    assert built.settings_obj.require_tls is False


def test_developer_contract_routes_are_client_registration_scoped_only() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    prefixes = admin_resource_path_prefixes(deployment)
    assert "/register" in deployment.active_routes
    assert "/.well-known/openid-configuration" in deployment.active_routes
    assert "/.well-known/jwks.json" in deployment.active_routes
    assert "/client" in prefixes
    assert "/clientregistration" in prefixes
    assert "/auditevent" in prefixes

    for forbidden in DEVELOPER_BACKEND_APP_CONTRACT.forbidden_route_prefixes:
        assert forbidden not in prefixes
    for route in DEVELOPER_BACKEND_APP_CONTRACT.forbidden_exact_routes:
        assert route not in deployment.active_routes


@pytest.mark.asyncio
async def test_developer_openapi_is_surface_constrained_and_openrpc_is_absent(
    tmp_path: Path,
) -> None:
    developer_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=developer_app), base_url="http://test"
    ) as client:
        openapi_response = await client.get("/openapi.json")
        openrpc_response = await client.get("/openrpc.json")

    assert openapi_response.status_code == 200
    assert openrpc_response.status_code == 404
    paths = openapi_response.json()["paths"]
    assert "/register" in paths
    assert "/.well-known/openid-configuration" in paths
    assert "/.well-known/jwks.json" in paths
    assert "/client" in paths
    assert "/clientregistration" in paths
    assert "/auditevent" in paths
    for forbidden in (
        "/tenant",
        "/user",
        "/service",
        "/login",
        "/authorize",
        "/token",
        "/introspect",
    ):
        assert forbidden not in paths


@pytest.mark.asyncio
async def test_developer_rpc_endpoint_is_not_supported(
    tmp_path: Path,
) -> None:
    developer_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=developer_app), base_url="http://test"
    ) as client:
        missing_key = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        register = await client.post("/register", json={})
        authorize = await client.get("/authorize")
        token = await client.post("/token", data={})

    assert missing_key.status_code == 404
    assert register.status_code != 404
    assert authorize.status_code == 404
    assert token.status_code == 404


@pytest.mark.asyncio
async def test_developer_rpc_dispatch_is_absent(
    tmp_path: Path,
) -> None:
    developer_app = build_app(_settings(tmp_path))
    headers = {"X-API-Key": "test-developer-key"}

    async with AsyncClient(
        transport=ASGITransport(app=developer_app), base_url="http://test"
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
async def test_developer_rest_control_plane_requires_admin_key(
    tmp_path: Path,
) -> None:
    developer_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=developer_app), base_url="http://test"
    ) as client:
        missing_key = await client.get("/client")
        invalid_key = await client.get(
            "/client", headers={"X-API-Key": "wrong-developer-key"}
        )
        tenant = await client.get(
            "/tenant", headers={"X-API-Key": "test-developer-key"}
        )
        service = await client.get(
            "/service", headers={"X-API-Key": "test-developer-key"}
        )
        login = await client.post("/login", json={})

    assert missing_key.status_code == 401
    assert missing_key.json()["error"] == "missing_admin_api_key"
    assert invalid_key.status_code == 403
    assert invalid_key.json()["error"] == "invalid_admin_api_key"
    assert tenant.status_code == 404
    assert service.status_code == 404
    assert login.status_code == 404
