"""ASGI entrypoint for the tenant admin Tigrbl Auth API surface."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tigrbl_auth.api.products import build_product_app
from tigrbl_auth.runtime import LazyASGIApplication

if TYPE_CHECKING:
    from tigrbl import TigrblApp

PRODUCT_SURFACE = "tenant-admin-api"


def build_app(settings_obj: object | None = None) -> "TigrblApp":
    return build_product_app(PRODUCT_SURFACE, settings_obj)


app = LazyASGIApplication(build_app)

__all__ = ["PRODUCT_SURFACE", "app", "build_app"]
