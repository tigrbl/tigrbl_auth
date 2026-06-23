from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.config.deployment import (
    DEFAULT_VALUES,
    PRODUCT_SURFACE_REGISTRY,
    SURFACE_SET_REGISTRY,
    resolve_deployment,
)
from tigrbl_auth.api.surfaces import admin_resource_path_prefixes
from tigrbl_auth.api import surfaces


ROOT = Path(__file__).resolve().parents[2]
API_PACKAGES = {
    "public-api": ("tigrbl_auth_api_public", ROOT / "pkgs/80-apis/tigrbl-auth-api-public/src"),
    "platform-admin-api": (
        "tigrbl_auth_api_platform_admin",
        ROOT / "pkgs/80-apis/tigrbl-auth-api-platform-admin/src",
    ),
    "tenant-admin-api": (
        "tigrbl_auth_api_tenant_admin",
        ROOT / "pkgs/80-apis/tigrbl-auth-api-tenant-admin/src",
    ),
    "developer-api": (
        "tigrbl_auth_api_developer",
        ROOT / "pkgs/80-apis/tigrbl-auth-api-developer/src",
    ),
    "service-admin-api": (
        "tigrbl_auth_api_service_admin",
        ROOT / "pkgs/80-apis/tigrbl-auth-api-service-admin/src",
    ),
    "resource-validation-api": (
        "tigrbl_auth_api_resource_validation",
        ROOT / "pkgs/80-apis/tigrbl-auth-api-resource-validation/src",
    ),
}


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        require_tls=False,
        admin_api_key="test-admin-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


def _import_api_package(product_surface: str):
    module_name, src_path = API_PACKAGES[product_surface]
    src = str(src_path)
    if src not in sys.path:
        sys.path.insert(0, src)
    return importlib.import_module(module_name)


def test_product_surfaces_are_registered_as_named_surface_sets() -> None:
    for product_surface in PRODUCT_SURFACE_REGISTRY:
        assert product_surface in SURFACE_SET_REGISTRY


def test_product_api_surface_resources_are_canonical_storage_tables() -> None:
    for resource in surfaces.TABLE_RESOURCES:
        assert resource.__module__.startswith("tigrbl_identity_storage.tables.")


@pytest.mark.parametrize("product_surface", sorted(API_PACKAGES))
def test_api_packages_build_surface_constrained_asgi_apps(
    product_surface: str, tmp_path: Path
) -> None:
    package = _import_api_package(product_surface)

    built = package.build_app(_settings(tmp_path))

    assert package.PRODUCT_SURFACE == product_surface
    assert callable(built)
    assert built.deployment.product_surface == product_surface


def test_public_and_resource_validation_surfaces_do_not_enable_control_plane() -> None:
    public = resolve_deployment(product_surface="public-api")
    validation = resolve_deployment(
        profile="production", product_surface="resource-validation-api"
    )

    assert public.surface_enabled("public-rest")
    assert public.plugin_mode == "public-only"
    assert not public.surface_enabled("admin-rest")
    assert "/login" in public.active_routes
    assert "/authorize" in public.active_routes

    assert validation.surface_enabled("public-rest")
    assert validation.plugin_mode == "public-only"
    assert not validation.surface_enabled("admin-rest")
    assert "/introspect" in validation.active_routes
    assert "/.well-known/jwks.json" in validation.active_routes
    assert "/login" not in validation.active_routes
    assert "/authorize" not in validation.active_routes
    assert "/register" not in validation.active_routes


def test_platform_admin_surface_owns_tenant_lifecycle_without_public_login_routes() -> (
    None
):
    deployment = resolve_deployment(product_surface="platform-admin-api")

    assert deployment.surface_enabled("admin-rest")
    assert deployment.plugin_mode == "admin-only"
    assert not deployment.surface_enabled("public-rest")
    assert "/admin/tenant" in admin_resource_path_prefixes(deployment)
    assert "/admin/identity" in admin_resource_path_prefixes(deployment)
    assert "/authsession" not in admin_resource_path_prefixes(deployment)
    assert "/tenant" not in admin_resource_path_prefixes(deployment)
    assert "/user" not in admin_resource_path_prefixes(deployment)
    assert "/login" not in deployment.active_routes
    assert "/register" not in deployment.active_routes


def test_tenant_admin_surface_excludes_platform_tenant_lifecycle() -> None:
    deployment = resolve_deployment(product_surface="tenant-admin-api")

    assert deployment.surface_enabled("admin-rest")
    assert deployment.plugin_mode == "admin-only"
    assert "/tenant" not in admin_resource_path_prefixes(deployment)
    assert "/user" in admin_resource_path_prefixes(deployment)
    assert "/authsession" not in admin_resource_path_prefixes(deployment)


def test_developer_and_service_admin_surfaces_are_product_filtered() -> None:
    developer = resolve_deployment(
        profile="production", product_surface="developer-api"
    )
    service = resolve_deployment(
        profile="production", product_surface="service-admin-api"
    )

    assert "/register" in developer.active_routes
    assert developer.plugin_mode == "mixed"
    assert developer.surface_enabled("admin-rest")
    assert "/authorize" not in developer.active_routes
    assert "/tenant" not in admin_resource_path_prefixes(developer)
    assert "/client" in admin_resource_path_prefixes(developer)

    assert "/introspect" in service.active_routes
    assert service.plugin_mode == "mixed"
    assert service.surface_enabled("admin-rest")
    assert "/login" not in service.active_routes
    assert "/serviceidentity" in admin_resource_path_prefixes(service)
    assert "/tenant" not in admin_resource_path_prefixes(service)


@pytest.mark.asyncio
async def test_product_apps_fail_closed_for_cross_surface_paths(tmp_path: Path) -> None:
    public = _import_api_package("public-api").build_app(_settings(tmp_path))
    platform = _import_api_package("platform-admin-api").build_app(_settings(tmp_path))
    tenant = _import_api_package("tenant-admin-api").build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=public), base_url="http://test"
    ) as client:
        public_rpc = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        public_tenant = await client.get("/tenant")

    async with AsyncClient(
        transport=ASGITransport(app=platform), base_url="http://test"
    ) as client:
        platform_login = await client.post("/login", json={})
        platform_tenant = await client.get("/tenant")
        platform_admin_tenants = await client.get("/admin/tenant")
        platform_user = await client.get("/user")
        platform_identity = await client.get("/admin/identity")
        platform_identities = await client.get("/admin/identities")
        platform_authsession = await client.get(
            "/authsession", headers={"X-API-Key": "test-admin-key"}
        )
        platform_rpc = await client.post("/rpc", json={})
        platform_openrpc = await client.get("/openrpc.json")

    async with AsyncClient(
        transport=ASGITransport(app=tenant), base_url="http://test"
    ) as client:
        tenant_tenant = await client.get(
            "/tenant", headers={"X-API-Key": "test-admin-key"}
        )

    assert public_rpc.status_code == 404
    assert public_tenant.status_code == 404
    assert platform_login.status_code == 404
    assert platform_tenant.status_code == 404
    assert platform_user.status_code == 404
    assert platform_admin_tenants.status_code == 401
    assert platform_identity.status_code == 401
    assert platform_identities.status_code == 401
    assert platform_authsession.status_code == 404
    assert platform_rpc.status_code == 404
    assert platform_openrpc.status_code == 404
    assert tenant_tenant.status_code == 404
