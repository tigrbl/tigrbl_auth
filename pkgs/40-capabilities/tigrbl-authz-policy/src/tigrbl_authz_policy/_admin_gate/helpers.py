from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Any

from tigrbl_identity_core import (
    headers_from_scope as _headers,
    json_response as _json_response,
    jsonrpc_error as _jsonrpc_error,
    read_http_body as _read_http_body,
    replay_http_body as _replay_http_body,
    sha256_text_digest as _digest,
)
from tigrbl_identity_runtime.deployment import ResolvedDeployment

from .constants import ADMIN_API_KEY_ENV, ADMIN_API_KEY_HEADER, logger


def _extract_credential(scope: dict[str, Any]) -> str | None:
    headers = _headers(scope)
    api_key = headers.get(ADMIN_API_KEY_HEADER)
    if api_key:
        return api_key
    authorization = headers.get("authorization", "")
    prefix = "bearer "
    if authorization.lower().startswith(prefix):
        token = authorization[len(prefix) :].strip()
        return token or None
    return None


def _control_plane_enabled(deployment: ResolvedDeployment) -> bool:
    return any(
        bool(deployment.surfaces.get(name, False))
        for name in (
            "surface_admin_enabled",
            "surface_diagnostics_enabled",
        )
    )


def _bootstrap_digest(settings_obj: object | None, enabled: bool) -> str | None:
    configured = os.environ.get(ADMIN_API_KEY_ENV) or getattr(
        settings_obj, "admin_api_key", None
    )
    if configured:
        return _digest(str(configured))
    if not enabled:
        return None

    key = secrets.token_urlsafe(32)
    digest = _digest(key)
    secret_dir = Path(
        str(getattr(settings_obj, "admin_api_key_dir", "runtime_secrets"))
    )
    secret_dir.mkdir(parents=True, exist_ok=True)
    digest_path = secret_dir / "admin_api_key.sha256"
    digest_path.write_text(digest + "\n", encoding="utf-8")
    try:
        digest_path.chmod(0o600)
    except OSError:
        pass
    logger.warning(
        "Generated bootstrap admin API key for local control-plane surfaces. "
        "Set TIGRBL_AUTH_ADMIN_API_KEY to replace it. bootstrap_key_sha256=%s",
        digest,
    )
    return digest


def _path_has_prefix(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


def _platform_admin_raw_table_path(path: str, deployment: ResolvedDeployment) -> bool:
    if getattr(deployment, "product_surface", None) != "platform-admin-api":
        return False
    return _path_has_prefix(path, "/tenant") or _path_has_prefix(path, "/user")
