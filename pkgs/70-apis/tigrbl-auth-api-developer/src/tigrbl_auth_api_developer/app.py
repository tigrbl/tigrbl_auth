"""ASGI entrypoint for the developer Tigrbl Auth API surface."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from tigrbl_auth.api.products import build_product_app
from tigrbl_auth.runtime import LazyASGIApplication

if TYPE_CHECKING:
    from tigrbl import TigrblApp

PRODUCT_SURFACE = "developer-api"


def _default_settings() -> object:
    from tigrbl_auth.config.settings import Settings

    settings = Settings()
    env_overrides = {
        "issuer": os.environ.get("AUTHN_ISSUER"),
        "protected_resource_identifier": os.environ.get(
            "TIGRBL_AUTH_PROTECTED_RESOURCE_IDENTIFIER"
        ),
        "deployment_profile": os.environ.get("TIGRBL_AUTH_PROFILE"),
        "require_tls": os.environ.get("TIGRBL_AUTH_REQUIRE_TLS"),
        "admin_api_key": os.environ.get("TIGRBL_AUTH_ADMIN_API_KEY"),
        "admin_api_key_dir": os.environ.get("TIGRBL_AUTH_ADMIN_API_KEY_DIR"),
    }
    for name, value in env_overrides.items():
        if value in {None, ""}:
            continue
        current = getattr(settings, name, None)
        if isinstance(current, bool):
            value = str(value).lower() in {"1", "true", "yes", "on"}
        setattr(settings, name, value)
    return settings


def build_app(settings_obj: object | None = None) -> "TigrblApp":
    if settings_obj is None:
        settings_obj = _default_settings()
    return build_product_app(PRODUCT_SURFACE, settings_obj)


app = LazyASGIApplication(build_app)

__all__ = ["PRODUCT_SURFACE", "app", "build_app"]
