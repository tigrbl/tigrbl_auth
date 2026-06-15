from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.surfaces import admin_resource_path_prefixes
from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment


ROOT = Path(__file__).resolve().parents[3]
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-api-service-admin" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

service_admin_package = import_module("tigrbl_auth_api_service_admin")
PRODUCT_SURFACE = service_admin_package.PRODUCT_SURFACE
SERVICE_ADMIN_API_CONTRACT = service_admin_package.SERVICE_ADMIN_API_CONTRACT
build_app = service_admin_package.build_app


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8018",
        protected_resource_identifier="http://localhost:8018/resource",
        require_tls=False,
        admin_api_key="test-service-admin-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


def _method_names(openrpc: dict[str, object]) -> set[str]:
    return {str(item["name"]) for item in openrpc.get("methods", [])}


def _rpc_discover_method_names(result: dict[str, object]) -> set[str]:
    return {str(item["name"]) for item in result.get("methods", [])}


def test_service_admin_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert PRODUCT_SURFACE == "service-admin-api"
    assert SERVICE_ADMIN_API_CONTRACT.product_surface == PRODUCT_SURFACE
    assert SERVICE_ADMIN_API_CONTRACT.intended_uix == "@tigrbl-auth/service-admin-uix"
    assert deployment.plugin_mode == "mixed"
    assert deployment.surface_enabled("public-rest")
    assert deployment.surface_enabled("admin-rpc")
    assert tuple(deployment.active_capabilities) == (
        SERVICE_ADMIN_API_CONTRACT.public_capabilities
    )
    assert tuple(deployment.allowed_admin_resources) == (
        SERVICE_ADMIN_API_CONTRACT.admin_resources
    )
    assert tuple(deployment.allowed_admin_rest_groups) == (
        SERVICE_ADMIN_API_CONTRACT.admin_rest_groups
    )


def test_service_admin_build_app_uses_environment_backed_default_settings() -> None:
    with patch.dict(
        "os.environ",
        {
            "AUTHN_ISSUER": "http://localhost:8018",
            "TIGRBL_AUTH_PROFILE": "production",
            "TIGRBL_AUTH_REQUIRE_TLS": "false",
            "TIGRBL_AUTH_ADMIN_API_KEY": "env-service-admin-key",
        },
    ):
        built = build_app()

    assert built.deployment.issuer == "http://localhost:8018"
    assert built.deployment.product_surface == PRODUCT_SURFACE
    assert built.settings_obj.admin_api_key == "env-service-admin-key"
    assert built.settings_obj.require_tls is False


def test_service_admin_contract_routes_are_service_scoped_only() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    prefixes = admin_resource_path_prefixes(deployment)
    assert "/introspect" in deployment.active_routes
    assert "/.well-known/oauth-protected-resource" in deployment.active_routes
    assert "/.well-known/openid-configuration" in deployment.active_routes
    assert "/.well-known/jwks.json" in deployment.active_routes
    assert "/service" in prefixes
    assert "/servicekey" in prefixes
    assert "/apikey" in prefixes
    assert "/tokenrecord" in prefixes
    assert "token.inspect" in deployment.active_openrpc_methods
    assert "token.list" in deployment.active_openrpc_methods

    for forbidden in SERVICE_ADMIN_API_CONTRACT.forbidden_route_prefixes:
        assert forbidden not in prefixes
    for route in SERVICE_ADMIN_API_CONTRACT.forbidden_exact_routes:
        assert route not in deployment.active_routes
    assert "tenant.list" not in deployment.active_openrpc_methods
    assert "client.list" not in deployment.active_openrpc_methods
    assert "identity.list" not in deployment.active_openrpc_methods


@pytest.mark.asyncio
async def test_service_admin_openapi_and_openrpc_are_surface_constrained(
    tmp_path: Path,
) -> None:
    service_admin_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=service_admin_app), base_url="http://test"
    ) as client:
        openapi_response = await client.get("/openapi.json")
        openrpc_response = await client.get("/openrpc.json")

    assert openapi_response.status_code == 200
    paths = openapi_response.json()["paths"]
    assert "/introspect" in paths
    assert "/.well-known/oauth-protected-resource" in paths
    assert "/.well-known/openid-configuration" in paths
    assert "/.well-known/jwks.json" in paths
    assert "/service" in paths
    assert "/servicekey" in paths
    assert "/apikey" in paths
    assert "/tokenrecord" in paths
    assert "/auditevent" in paths
    for forbidden in (
        "/tenant",
        "/user",
        "/client",
        "/clientregistration",
        "/login",
        "/authorize",
        "/token",
        "/register",
    ):
        assert forbidden not in paths

    assert openrpc_response.status_code == 200
    methods = _method_names(openrpc_response.json())
    assert {"Service.list", "ServiceKey.list", "ApiKey.list", "TokenRecord.list"}.issubset(
        methods
    )
    assert "Tenant.list" not in methods
    assert "User.list" not in methods
    assert "Client.list" not in methods
    assert "ClientRegistration.list" not in methods


@pytest.mark.asyncio
async def test_service_admin_rpc_requires_key_and_reports_service_methods(
    tmp_path: Path,
) -> None:
    service_admin_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=service_admin_app), base_url="http://test"
    ) as client:
        missing_key = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        valid_key = await client.post(
            "/rpc",
            headers={"X-API-Key": "test-service-admin-key"},
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        introspect = await client.post("/introspect", data={})
        token = await client.post("/token", data={})

    assert missing_key.status_code == 401
    assert missing_key.json()["error"] == "missing_admin_api_key"
    assert valid_key.status_code == 200
    result = valid_key.json()["result"]
    assert result["deployment"]["plugin_mode"] == "mixed"
    assert result["deployment"]["surface_sets"] == ["public-rest", "admin-rpc"]
    assert "/introspect" in result["deployment"]["active_routes"]
    methods = _rpc_discover_method_names(result)
    assert "token.inspect" in methods
    assert "token.list" in methods
    assert "tenant.list" not in methods
    assert "client.list" not in methods
    assert "identity.list" not in methods
    assert introspect.status_code == 400
    assert token.status_code == 404


@pytest.mark.asyncio
async def test_service_admin_rpc_dispatch_fails_closed_for_cross_surface_methods(
    tmp_path: Path,
) -> None:
    service_admin_app = build_app(_settings(tmp_path))
    headers = {"X-API-Key": "test-service-admin-key"}

    async with AsyncClient(
        transport=ASGITransport(app=service_admin_app), base_url="http://test"
    ) as client:
        allowed = await client.post(
            "/rpc",
            headers=headers,
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        platform_method = await client.post(
            "/rpc",
            headers=headers,
            json={"jsonrpc": "2.0", "method": "tenant.list", "params": {}, "id": 2},
        )
        developer_method = await client.post(
            "/rpc",
            headers=headers,
            json={"jsonrpc": "2.0", "method": "client.list", "params": {}, "id": 3},
        )

    assert allowed.status_code == 200
    assert allowed.json()["result"]["deployment"]["plugin_mode"] == "mixed"
    assert platform_method.status_code == 200
    assert platform_method.json()["error"]["code"] == -32601
    assert platform_method.json()["error"]["message"] == "Method not found"
    assert developer_method.status_code == 200
    assert developer_method.json()["error"]["code"] == -32601
    assert developer_method.json()["error"]["message"] == "Method not found"


@pytest.mark.asyncio
async def test_service_admin_rest_control_plane_requires_admin_key(
    tmp_path: Path,
) -> None:
    service_admin_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=service_admin_app), base_url="http://test"
    ) as client:
        missing_key = await client.get("/service")
        invalid_key = await client.get(
            "/service", headers={"X-API-Key": "wrong-service-admin-key"}
        )
        client_resource = await client.get(
            "/client", headers={"X-API-Key": "test-service-admin-key"}
        )
        tenant = await client.get(
            "/tenant", headers={"X-API-Key": "test-service-admin-key"}
        )
        login = await client.post("/login", json={})

    assert missing_key.status_code == 401
    assert missing_key.json()["error"] == "missing_admin_api_key"
    assert invalid_key.status_code == 403
    assert invalid_key.json()["error"] == "invalid_admin_api_key"
    assert client_resource.status_code == 404
    assert tenant.status_code == 404
    assert login.status_code == 404
