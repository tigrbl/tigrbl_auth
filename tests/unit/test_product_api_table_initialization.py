from __future__ import annotations

import pytest

from tigrbl_auth.api.surfaces import (
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


def test_product_api_table_initialization_t0_exports_manifest_surface() -> None:
    deployment = resolve_deployment(product_surface="public-api")

    assert callable(table_initialization_manifest)
    assert callable(assert_table_initialization_scope)
    assert table_initialization_manifest(deployment) == {
        "product_surface": "public-api",
        "required_table_resources": [],
    }


@pytest.mark.parametrize("product_surface", sorted(PRODUCT_SURFACE_REGISTRY))
def test_product_api_table_initialization_t1_matches_product_contract(
    product_surface: str,
) -> None:
    deployment = resolve_deployment(product_surface=product_surface)
    expected = tuple(PRODUCT_SURFACE_REGISTRY[product_surface]["admin_resources"])
    router = build_surface_api(deployment=deployment)

    assert deployment.required_table_resources == expected
    assert tuple(table_initialization_manifest(deployment)["required_table_resources"]) == expected
    assert _route_model_names(router).issubset(set(expected))
    assert_table_initialization_scope(deployment, tuple(expected))
