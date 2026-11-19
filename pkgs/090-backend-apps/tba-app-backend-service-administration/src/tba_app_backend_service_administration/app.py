"""ASGI entrypoint for the service admin TBA backend application."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from tba_app_backend_core import build_product_app
from tba_app_backend_service_administration.contract import (
    SERVICE_ADMIN_BACKEND_APP_CONTRACT,
)
from tba_auth.runtime import LazyASGIApplication

if TYPE_CHECKING:
    from tigrbl import TigrblApp

PRODUCT_SURFACE = "service-admin-app"


def _default_settings() -> object:
    from tba_auth.config.settings import Settings

    settings = Settings()
    env_overrides = {
        "issuer": os.environ.get("AUTHN_ISSUER"),
        "protected_resource_identifier": os.environ.get(
            "TBA_AUTH_PROTECTED_RESOURCE_IDENTIFIER"
        ),
        "deployment_profile": os.environ.get("TBA_AUTH_PROFILE"),
        "require_tls": os.environ.get("TBA_AUTH_REQUIRE_TLS"),
        "admin_api_key": os.environ.get("TBA_AUTH_ADMIN_API_KEY"),
        "admin_api_key_dir": os.environ.get("TBA_AUTH_ADMIN_API_KEY_DIR"),
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
    return build_product_app(
        PRODUCT_SURFACE, settings_obj, contract=SERVICE_ADMIN_BACKEND_APP_CONTRACT
    )


app = LazyASGIApplication(build_app)

__all__ = ["PRODUCT_SURFACE", "app", "build_app"]
