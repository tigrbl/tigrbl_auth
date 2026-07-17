from __future__ import annotations

from types import SimpleNamespace

import pytest

from tigrbl_auth.api import lifecycle
from tigrbl_auth.api.surfaces import (
    TableInitializationScopeError,
    assert_table_initialization_scope,
    build_surface_api,
    table_initialization_manifest,
)
from tigrbl_auth.config.deployment import PRODUCT_SURFACE_REGISTRY, resolve_deployment


def _route_model_names(router: object) -> set[str]:
    names: set[str] = set()
    for route in getattr(router, "_routes", []):
        model = getattr(route, "tigrbl_model", None)
        name = getattr(model, "__name__", None)
        if isinstance(name, str):
            names.add(name)
    return names


def test_backend_app_table_initialization_t0_exports_manifest_surface() -> None:
    deployment = resolve_deployment(product_surface="public-app")

    assert callable(table_initialization_manifest)
    assert callable(assert_table_initialization_scope)
    assert table_initialization_manifest(deployment) == {
        "product_surface": "public-app",
        "required_table_resources": [],
    }


@pytest.mark.parametrize("product_surface", sorted(PRODUCT_SURFACE_REGISTRY))
def test_backend_app_table_initialization_t1_matches_product_contract(
    product_surface: str,
) -> None:
    deployment = resolve_deployment(product_surface=product_surface)
    expected = tuple(PRODUCT_SURFACE_REGISTRY[product_surface]["admin_resources"])
    router = build_surface_api(deployment=deployment)

    assert deployment.required_table_resources == expected
    assert (
        tuple(table_initialization_manifest(deployment)["required_table_resources"])
        == expected
    )
    assert _route_model_names(router).issubset(set(expected))
    assert_table_initialization_scope(deployment, tuple(expected))


def test_backend_app_table_initialization_t2_fails_closed_on_scope_mismatch() -> None:
    public = resolve_deployment(product_surface="public-app")
    tenant = resolve_deployment(product_surface="tenant-admin-app")
    tenant_expected = tuple(
        PRODUCT_SURFACE_REGISTRY["tenant-admin-app"]["admin_resources"]
    )

    with pytest.raises(TableInitializationScopeError, match="unexpected"):
        assert_table_initialization_scope(public, ("Tenant",))

    with pytest.raises(TableInitializationScopeError, match="missing"):
        assert_table_initialization_scope(tenant, tenant_expected[:-1])


@pytest.mark.asyncio
async def test_backend_app_table_initialization_t2_startup_uses_mounted_surface_router(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    class ProductSurfaceRouter:
        def initialize(self) -> None:
            calls.append("product-surface")

    async def _noop(*args: object, **kwargs: object) -> None:
        return None

    def _activate_runtime_tables() -> None:
        calls.append("storage-runtime")

    monkeypatch.setattr(lifecycle, "apply_all_async", _noop)
    monkeypatch.setattr(
        lifecycle,
        "initializeIdentityRuntimeTables",
        _activate_runtime_tables,
    )
    monkeypatch.setattr(lifecycle, "ensure_default_superuser_async", _noop)
    SimpleNamespace(
        state=SimpleNamespace(tigrbl_auth_surface_router=ProductSurfaceRouter())
    )

    monkeypatch.setattr(lifecycle, "surface_api", ProductSurfaceRouter())

    await lifecycle._startup()

    assert calls == ["storage-runtime", "product-surface"]
