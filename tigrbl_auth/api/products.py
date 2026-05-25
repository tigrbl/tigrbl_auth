"""Product-surface app factories for split Tigrbl Auth API front doors."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tigrbl_auth.config.deployment import PRODUCT_SURFACE_REGISTRY, resolve_deployment

if TYPE_CHECKING:
    from tigrbl import TigrblApp


def build_product_app(
    product_surface: str,
    settings_obj: object | None = None,
) -> "TigrblApp":
    """Build the shared ASGI app constrained to one product API surface."""
    from tigrbl_auth.api.app import build_app

    if product_surface not in PRODUCT_SURFACE_REGISTRY:
        raise ValueError(f"unknown tigrbl_auth product surface: {product_surface}")
    deployment = resolve_deployment(
        settings_obj,
        product_surface=product_surface,
        runtime_style="standalone",
    )
    return build_app(settings_obj, deployment=deployment)


__all__ = ["build_product_app"]
