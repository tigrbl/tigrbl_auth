"""Tigrbl application entrypoint helpers for the package-level ASGI surface."""

from __future__ import annotations

from tigrbl_auth.api.app import build_app, build_application_runtime_plan, _load_default_settings
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.runtime import LazyASGIApplication


def _package_default_profile() -> str:
    settings_obj = _load_default_settings()
    configured = str(getattr(settings_obj, "deployment_profile", "baseline") or "baseline")
    return configured if configured != "baseline" else "production"


def _build_package_app():
    settings_obj = _load_default_settings()
    deployment = resolve_deployment(settings_obj, profile=_package_default_profile())
    return build_app(settings_obj, deployment=deployment)


app = LazyASGIApplication(_build_package_app)

__all__ = ["app", "build_app", "build_application_runtime_plan"]
