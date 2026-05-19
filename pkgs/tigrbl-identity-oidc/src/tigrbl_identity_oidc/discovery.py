"""Compatibility facade for OIDC discovery.

When the full runtime stack is importable, this module re-exports the canonical
router-backed implementation. In dependency-light checkpoint environments, it
falls back to pure metadata helpers so discovery snapshots and unit tests can be
exercised without Tigrbl/SQLAlchemy.
"""

from __future__ import annotations

try:  # pragma: no cover - exercised when runtime dependencies are installed
    from tigrbl_auth.standards.oidc.discovery import (
        ISSUER,
        JWKS_PATH,
        _build_openid_config,
        _cached_openid_config,
        _settings_signature,
        api,
        include_oidc_discovery,
        refresh_discovery_cache,
        router,
    )
except Exception:  # pragma: no cover - dependency-light fallback
    import json
    from functools import lru_cache
    from typing import Any

    from tigrbl_auth.config.deployment import resolve_deployment
    from tigrbl_auth.config.settings import settings
    from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config
    from tigrbl_auth.standards.oauth2.rfc8414_metadata import ISSUER, JWKS_PATH

    api = None
    router = None

    def _settings_signature(
        settings_obj: object | None = None,
        *,
        profile: str | None = None,
        flag_overrides: dict[str, Any] | None = None,
    ) -> str:
        deployment = resolve_deployment(settings_obj or settings, profile=profile, flag_overrides=flag_overrides)
        return json.dumps(deployment.to_manifest(), sort_keys=True)

    def _build_openid_config(
        settings_obj: object | None = None,
        *,
        profile: str | None = None,
        flag_overrides: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_openid_config(settings_obj or settings, profile=profile, flag_overrides=flag_overrides)

    @lru_cache(maxsize=8)
    def _cached_openid_config(sig: str) -> dict[str, Any]:
        return _build_openid_config()

    def refresh_discovery_cache() -> None:
        _cached_openid_config.cache_clear()

    def include_oidc_discovery(app) -> None:
        return None

__all__ = [
    "api",
    "router",
    "JWKS_PATH",
    "ISSUER",
    "include_oidc_discovery",
    "refresh_discovery_cache",
    "_build_openid_config",
    "_cached_openid_config",
    "_settings_signature",
]
