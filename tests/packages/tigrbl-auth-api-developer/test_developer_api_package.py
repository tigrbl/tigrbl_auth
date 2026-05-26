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
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-api-developer" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

developer_package = import_module("tigrbl_auth_api_developer")
PRODUCT_SURFACE = developer_package.PRODUCT_SURFACE
DEVELOPER_API_CONTRACT = developer_package.DEVELOPER_API_CONTRACT
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


def _method_names(openrpc: dict[str, object]) -> set[str]:
    return {str(item["name"]) for item in openrpc.get("methods", [])}


def _rpc_discover_method_names(result: dict[str, object]) -> set[str]:
    return {str(item["name"]) for item in result.get("methods", [])}


def test_developer_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert PRODUCT_SURFACE == "developer-api"
    assert DEVELOPER_API_CONTRACT.product_surface == PRODUCT_SURFACE
    assert DEVELOPER_API_CONTRACT.intended_uix == "@tigrbl-auth/developer-uix"
    assert deployment.plugin_mode == "mixed"
    assert deployment.surface_enabled("public-rest")
    assert deployment.surface_enabled("admin-rpc")
    assert tuple(deployment.active_capabilities) == (
        DEVELOPER_API_CONTRACT.public_capabilities
    )
    assert tuple(deployment.allowed_admin_resources) == (
        DEVELOPER_API_CONTRACT.admin_resources
    )
    assert tuple(deployment.allowed_admin_rest_groups) == (
        DEVELOPER_API_CONTRACT.admin_rest_groups
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
    assert "client.registration.upsert" in deployment.active_openrpc_methods
    assert "client.list" in deployment.active_openrpc_methods

    for forbidden in DEVELOPER_API_CONTRACT.forbidden_route_prefixes:
        assert forbidden not in prefixes
    for route in DEVELOPER_API_CONTRACT.forbidden_exact_routes:
        assert route not in deployment.active_routes
    assert "tenant.list" not in deployment.active_openrpc_methods
    assert "identity.list" not in deployment.active_openrpc_methods
    assert "token.inspect" not in deployment.active_openrpc_methods


@pytest.mark.asyncio
async def test_developer_openapi_and_openrpc_are_surface_constrained(
    tmp_path: Path,
) -> None:
    developer_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=developer_app), base_url="http://test"
    ) as client:
        openapi_response = await client.get("/openapi.json")
        openrpc_response = await client.get("/openrpc.json")

    assert openapi_response.status_code == 200
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

    assert openrpc_response.status_code == 200
    methods = _method_names(openrpc_response.json())
    assert {"Client.list", "ClientRegistration.list", "AuditEvent.list"}.issubset(
        methods
    )
    assert "Tenant.list" not in methods
    assert "User.list" not in methods
    assert "Service.list" not in methods


@pytest.mark.asyncio
async def test_developer_rpc_requires_key_and_reports_client_methods(
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
        valid_key = await client.post(
            "/rpc",
            headers={"X-API-Key": "test-developer-key"},
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        register = await client.post("/register", json={})
        authorize = await client.get("/authorize")
        token = await client.post("/token", data={})

    assert missing_key.status_code == 401
    assert missing_key.json()["error"] == "missing_admin_api_key"
    assert valid_key.status_code == 200
    result = valid_key.json()["result"]
    assert result["deployment"]["plugin_mode"] == "mixed"
    assert result["deployment"]["surface_sets"] == ["public-rest", "admin-rpc"]
    assert "/register" in result["deployment"]["active_routes"]
    methods = _rpc_discover_method_names(result)
    assert "client.list" in methods
    assert "client.registration.upsert" in methods
    assert "tenant.list" not in methods
    assert "identity.list" not in methods
    assert "token.inspect" not in methods
    assert register.status_code != 404
    assert authorize.status_code == 404
    assert token.status_code == 404


@pytest.mark.asyncio
async def test_developer_rpc_dispatch_fails_closed_for_cross_surface_methods(
    tmp_path: Path,
) -> None:
    developer_app = build_app(_settings(tmp_path))
    headers = {"X-API-Key": "test-developer-key"}

    async with AsyncClient(
        transport=ASGITransport(app=developer_app), base_url="http://test"
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
        service_method = await client.post(
            "/rpc",
            headers=headers,
            json={"jsonrpc": "2.0", "method": "token.inspect", "params": {}, "id": 3},
        )

    assert allowed.status_code == 200
    assert allowed.json()["result"]["deployment"]["plugin_mode"] == "mixed"
    assert platform_method.status_code == 200
    assert platform_method.json()["error"]["code"] == -32601
    assert platform_method.json()["error"]["message"] == "Method not found"
    assert service_method.status_code == 200
    assert service_method.json()["error"]["code"] == -32601
    assert service_method.json()["error"]["message"] == "Method not found"


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
