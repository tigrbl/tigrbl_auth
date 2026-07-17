"""Backend-app factories for composed Tigrbl Auth deployment surfaces."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tigrbl_identity_runtime.deployment import (
    PRODUCT_SURFACE_REGISTRY,
    resolve_deployment,
)

if TYPE_CHECKING:
    from tigrbl import TigrblApp


def _validate_backend_app_contract(contract: object, deployment: object) -> None:
    expected_surface = getattr(contract, "product_surface", None)
    actual_surface = getattr(deployment, "product_surface", None)
    if expected_surface != actual_surface:
        raise ValueError(
            "backend-app contract product surface does not match deployment: "
            f"{expected_surface!r} != {actual_surface!r}"
        )

    declared_routers = tuple(getattr(contract, "mounted_router_packages", ()))
    resolved_routers = tuple(getattr(deployment, "router_packages", ()))
    if declared_routers != resolved_routers:
        raise ValueError(
            "backend-app contract router closure does not match deployment: "
            f"{declared_routers!r} != {resolved_routers!r}"
        )


def build_product_app(
    product_surface: str,
    settings_obj: object | None = None,
    *,
    contract: object | None = None,
) -> "TigrblApp":
    """Build the shared ASGI app constrained to one backend-app surface."""
    from tigrbl_identity_server.api.app import build_app

    if product_surface not in PRODUCT_SURFACE_REGISTRY:
        raise ValueError(f"unknown tigrbl_auth product surface: {product_surface}")
    deployment = resolve_deployment(
        settings_obj,
        product_surface=product_surface,
        runtime_style="standalone",
    )
    if contract is not None:
        _validate_backend_app_contract(contract, deployment)
    return build_app(settings_obj, deployment=deployment)


__all__ = ["build_product_app"]
