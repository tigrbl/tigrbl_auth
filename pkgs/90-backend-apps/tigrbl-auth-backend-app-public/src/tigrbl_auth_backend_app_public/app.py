"""ASGI entrypoint for the public Tigrbl Auth backend application."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from tigrbl_auth.backend_apps import build_product_app
from tigrbl_auth_backend_app_public.contract import PUBLIC_BACKEND_APP_CONTRACT
from tigrbl_auth.runtime import LazyASGIApplication
from tigrbl_auth_backend_app_public.openapi import patch_public_openapi

if TYPE_CHECKING:
    from tigrbl import TigrblApp

PRODUCT_SURFACE = "public-app"


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
        "session_cookie_force_secure": os.environ.get(
            "TIGRBL_AUTH_SESSION_COOKIE_FORCE_SECURE"
        ),
        "enable_rfc9207": os.environ.get("TIGRBL_AUTH_ENABLE_RFC9207"),
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
    return patch_public_openapi(
        build_product_app(
            PRODUCT_SURFACE, settings_obj, contract=PUBLIC_BACKEND_APP_CONTRACT
        )
    )


app = LazyASGIApplication(build_app)

__all__ = ["PRODUCT_SURFACE", "app", "build_app"]
