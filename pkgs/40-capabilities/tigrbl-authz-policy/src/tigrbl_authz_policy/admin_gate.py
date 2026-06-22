"""Generated-surface admin gate policy helpers."""

from __future__ import annotations

import hmac
import logging
import os
import secrets
from pathlib import Path
from typing import Any, Awaitable, Callable, Iterable

from tigrbl.security import APIKey, HTTPBearer, Security
from tigrbl_identity_core import (
    headers_from_scope as _headers,
    json_response as _json_response,
    jsonrpc_error as _jsonrpc_error,
    read_http_body as _read_http_body,
    replay_http_body as _replay_http_body,
    sha256_text_digest as _digest,
)
from tigrbl_identity_runtime.deployment import ResolvedDeployment
from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

ADMIN_API_KEY_ENV = "TIGRBL_AUTH_ADMIN_API_KEY"
ADMIN_API_KEY_HEADER = "x-api-key"
ADMIN_BEARER_SCHEME = "AdminBearer"
ADMIN_HEADER_SCHEME = "AdminApiKeyHeader"
ADMIN_SECURITY_SCHEMES: dict[str, dict[str, Any]] = {
    ADMIN_HEADER_SCHEME: {"type": "apiKey", "in": "header", "name": "X-API-Key"},
    ADMIN_BEARER_SCHEME: {"type": "http", "scheme": "bearer"},
}
ADMIN_SECURITY_REQUIREMENT: list[dict[str, list[Any]]] = [
    {ADMIN_HEADER_SCHEME: []},
    {ADMIN_BEARER_SCHEME: []},
]
ADMIN_OPENAPI_SECURITY_DEPENDENCIES = (
    Security(
        APIKey(
            scheme_name=ADMIN_HEADER_SCHEME,
            name="X-API-Key",
            auto_error=False,
        )
    ),
    Security(
        HTTPBearer(
            scheme_name=ADMIN_BEARER_SCHEME,
            auto_error=False,
        )
    ),
)
logger = logging.getLogger(__name__)


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


class AdminGate:
    """ASGI gate for generated local control-plane surfaces."""

    def __init__(
        self,
        app: Any,
        *,
        deployment: ResolvedDeployment,
        settings_obj: object | None = None,
        admin_path_prefixes: Iterable[str] = (),
        diagnostics_prefix: str = "/system",
    ) -> None:
        self.app = app
        self.deployment = deployment
        self.settings_obj = settings_obj
        self.admin_path_prefixes = tuple(dict.fromkeys(admin_path_prefixes))
        self.diagnostics_prefix = diagnostics_prefix
        self.enabled = _control_plane_enabled(deployment)
        self._digest = _bootstrap_digest(settings_obj, self.enabled)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.app, name)

    def _requires_admin(self, path: str) -> bool:
        if not self.enabled:
            return False
        if self.deployment.flag_enabled(
            "surface_diagnostics_enabled"
        ) and _path_has_prefix(path, self.diagnostics_prefix):
            return True
        if self.deployment.flag_enabled("surface_admin_enabled"):
            return any(
                _path_has_prefix(path, prefix) for prefix in self.admin_path_prefixes
            )
        return False

    def _disabled_control_plane_path(self, path: str) -> bool:
        if _platform_admin_raw_table_path(path, self.deployment):
            return True
        if not self.deployment.flag_enabled(
            "surface_diagnostics_enabled"
        ) and _path_has_prefix(path, self.diagnostics_prefix):
            return True
        return False

    async def _dispatch_registry_rpc(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> bool:
        return False

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        path = str(scope.get("path") or "")
        if self._disabled_control_plane_path(path):
            status, headers, body = _json_response(404, {"detail": "Not Found"})
            await send(
                {"type": "http.response.start", "status": status, "headers": headers}
            )
            await send({"type": "http.response.body", "body": body})
            return

        if self._requires_admin(path):
            credential = _extract_credential(scope)
            authorized = False
            if (
                credential
                and self._digest
                and hmac.compare_digest(_digest(credential), self._digest)
            ):
                authorized = True
            if not authorized:
                request = _scope_request(scope)
                try:
                    authorized = (
                        await resolve_admin_user_from_request(request) is not None
                    )
                except (
                    Exception
                ):  # pragma: no cover - fail closed on middleware auth errors
                    authorized = False
            if not authorized:
                if credential:
                    status, headers, body = _json_response(
                        403, {"error": "invalid_admin_api_key"}
                    )
                else:
                    status, headers, body = _json_response(
                        401, {"error": "missing_admin_api_key"}
                    )
                await send(
                    {
                        "type": "http.response.start",
                        "status": status,
                        "headers": headers,
                    }
                )
                await send({"type": "http.response.body", "body": body})
                return

        await self.app(scope, receive, send)


class _ScopeRequest:
    def __init__(self, scope: dict[str, Any]) -> None:
        self.scope = scope
        self.state = type("State", (), {})()
        self.cookies = self._parse_cookies()

    def _parse_cookies(self) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for key, value in self.scope.get("headers", []):
            if key.decode("latin-1").lower() != "cookie":
                continue
            raw = value.decode("latin-1")
            for chunk in raw.split(";"):
                if "=" not in chunk:
                    continue
                name, cookie_value = chunk.split("=", 1)
                parsed[name.strip()] = cookie_value.strip()
        return parsed


def _scope_request(scope: dict[str, Any]) -> Any:
    return _ScopeRequest(scope)


__all__ = [
    "ADMIN_SECURITY_REQUIREMENT",
    "ADMIN_SECURITY_SCHEMES",
    "ADMIN_OPENAPI_SECURITY_DEPENDENCIES",
    "AdminGate",
]
