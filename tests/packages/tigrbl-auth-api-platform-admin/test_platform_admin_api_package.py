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
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-api-platform-admin" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

platform_admin_package = import_module("tigrbl_auth_api_platform_admin")
PRODUCT_SURFACE = platform_admin_package.PRODUCT_SURFACE
PLATFORM_ADMIN_API_CONTRACT = platform_admin_package.PLATFORM_ADMIN_API_CONTRACT
build_app = platform_admin_package.build_app


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


def test_platform_admin_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert PRODUCT_SURFACE == "platform-admin-api"
    assert PLATFORM_ADMIN_API_CONTRACT.product_surface == PRODUCT_SURFACE
    assert PLATFORM_ADMIN_API_CONTRACT.intended_uix == (
        "@tigrbl-auth/platform-admin-uix"
    )
    assert deployment.plugin_mode == "admin-only"
    assert deployment.surface_enabled("admin-rest")
    assert not deployment.surface_enabled("public-rest")
    assert tuple(deployment.allowed_admin_resources) == (
        PLATFORM_ADMIN_API_CONTRACT.admin_resources
    )
    assert tuple(deployment.allowed_admin_rest_groups) == (
        PLATFORM_ADMIN_API_CONTRACT.admin_rest_groups
    )


def test_platform_admin_build_app_uses_environment_backed_default_settings() -> None:
    with patch.dict(
        "os.environ",
        {
            "AUTHN_ISSUER": "http://localhost:8015",
            "TIGRBL_AUTH_PROFILE": "production",
            "TIGRBL_AUTH_REQUIRE_TLS": "false",
            "TIGRBL_AUTH_ADMIN_API_KEY": "env-platform-admin-key",
        },
    ):
        built = build_app()

    assert built.deployment.issuer == "http://localhost:8015"
    assert built.deployment.product_surface == PRODUCT_SURFACE
    assert built.settings_obj.admin_api_key == "env-platform-admin-key"
    assert built.settings_obj.require_tls is False


def test_platform_admin_contract_routes_are_platform_control_plane_only() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert "/admin/tenant" in admin_resource_path_prefixes(deployment)
    assert "/admin/realm" in admin_resource_path_prefixes(deployment)
    assert "/admin/identity" in admin_resource_path_prefixes(deployment)
    assert "/realm" not in admin_resource_path_prefixes(deployment)
    assert "/tenant" not in admin_resource_path_prefixes(deployment)
    assert "/user" not in admin_resource_path_prefixes(deployment)
    assert "/client" not in admin_resource_path_prefixes(deployment)

    for route in PLATFORM_ADMIN_API_CONTRACT.forbidden_exact_routes:
        assert route not in deployment.active_routes


@pytest.mark.asyncio
async def test_platform_admin_openapi_is_rest_control_plane_only(
    tmp_path: Path,
) -> None:
    platform_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=platform_app), base_url="http://test"
    ) as client:
        openapi_response = await client.get("/openapi.json")
        openrpc_response = await client.get("/openrpc.json")
        rpc_response = await client.post("/rpc", json={})

    assert openapi_response.status_code == 200
    paths = openapi_response.json()["paths"]
    assert "/tenant" not in paths
    assert "/realm" not in paths
    assert "/user" not in paths
    assert "/admin/realm" in paths
    assert "/admin/realm/{realm_id}" in paths
    assert "/admin/realm/{realm_id}/tenant" in paths
    assert "/admin/identity" in paths
    assert "/admin/identity/{item_id}" in paths
    assert "/admin/identities" in paths
    assert "/admin/identities/{user_id}" in paths
    assert "/authsession" not in paths
    assert "/authsession/{item_id}" not in paths
    assert "/auditevent" in paths
    assert "/admin/tenant" in paths
    assert "/client" not in paths
    for path, methods in paths.items():
        if path.startswith("/admin/auth/"):
            for operation in methods.values():
                assert operation["tags"] == ["Admin Auth"]
    for route in PLATFORM_ADMIN_API_CONTRACT.forbidden_exact_routes:
        assert route not in paths
    schemas = openapi_response.json()["components"]["schemas"]
    assert "AdminTenantOut" in schemas
    assert "AdminRealmOut" in schemas
    assert "UserCreateRequest" in schemas
    assert "UserUpdateRequest" in schemas
    assert paths["/admin/tenant"]["post"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == "#/components/schemas/AdminTenantOut"
    assert (
        paths["/admin/identity"]["post"]["requestBody"]["content"][
            "application/json"
        ]["schema"]["$ref"]
        == "#/components/schemas/UserCreateRequest"
    )
    assert (
        paths["/admin/identities"]["get"]["responses"]["200"]["content"][
            "application/json"
        ]["schema"]["items"]["$ref"]
        == "#/components/schemas/AdminIdentityOut"
    )
    assert (
        paths["/admin/identities"]["post"]["responses"]["200"]["content"][
            "application/json"
        ]["schema"]["$ref"]
        == "#/components/schemas/AdminIdentityOut"
    )

    assert openrpc_response.status_code == 404
    assert rpc_response.status_code == 404


@pytest.mark.asyncio
async def test_platform_admin_cors_allows_uix_origin_on_error_responses(
    tmp_path: Path,
) -> None:
    platform_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=platform_app), base_url="http://test"
    ) as client:
        preflight = await client.options(
            "/admin/auth/login",
            headers={
                "origin": "http://localhost:3011",
                "access-control-request-method": "POST",
                "access-control-request-headers": "content-type",
            },
        )
        anonymous = await client.get(
            "/admin/identities",
            headers={"origin": "http://localhost:3011"},
        )

    assert preflight.status_code == 204
    assert preflight.headers["access-control-allow-origin"] == "http://localhost:3011"
    assert preflight.headers["access-control-allow-credentials"] == "true"
    assert "content-type" in preflight.headers["access-control-allow-headers"]
    assert anonymous.status_code == 401
    assert anonymous.headers["access-control-allow-origin"] == "http://localhost:3011"
    assert anonymous.headers["access-control-allow-credentials"] == "true"


@pytest.mark.asyncio
async def test_platform_admin_rest_control_plane_excludes_rpc(
    tmp_path: Path,
) -> None:
    platform_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=platform_app), base_url="http://test"
    ) as client:
        rpc = await client.post(
            "/rpc", headers={"X-API-Key": "test-platform-admin-key"}, json={}
        )
        openrpc = await client.get("/openrpc.json")
        login = await client.post("/login", json={})
        register = await client.post("/register", json={})
        token = await client.post("/token", data={})

    assert rpc.status_code == 404
    assert openrpc.status_code == 404
    assert login.status_code == 404
    assert register.status_code == 404
    assert token.status_code == 404


@pytest.mark.asyncio
async def test_platform_admin_rest_control_plane_requires_admin_key(
    tmp_path: Path,
) -> None:
    platform_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=platform_app), base_url="http://test"
    ) as client:
        missing_key = await client.get("/admin/identities")
        invalid_key = await client.get(
            "/admin/identities",
            headers={"X-API-Key": "wrong-platform-admin-key"},
        )
        raw_tenant = await client.get(
            "/tenant", headers={"X-API-Key": "test-platform-admin-key"}
        )
        raw_realm = await client.get(
            "/realm", headers={"X-API-Key": "test-platform-admin-key"}
        )
        raw_user = await client.get(
            "/user", headers={"X-API-Key": "test-platform-admin-key"}
        )
        raw_authsession = await client.get(
            "/authsession", headers={"X-API-Key": "test-platform-admin-key"}
        )
        tenant_admin_route = await client.post("/admin/tenant", json={})
        login = await client.post("/login", json={})
        token = await client.post("/token", data={})

    assert missing_key.status_code == 401
    assert missing_key.json()["error"] == "missing_admin_api_key"
    assert invalid_key.status_code == 403
    assert invalid_key.json()["error"] == "invalid_admin_api_key"
    assert tenant_admin_route.status_code == 401
    assert raw_tenant.status_code == 404
    assert raw_realm.status_code == 404
    assert raw_user.status_code == 404
    assert raw_authsession.status_code == 404
    assert login.status_code == 404
    assert token.status_code == 404
