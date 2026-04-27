from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import secrets
from pathlib import Path
from typing import Any, Iterable

from tigrbl.security import Security

from tigrbl_auth.config.deployment import ResolvedDeployment

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


class AdminOpenAPISecurityDependency:
    def __init__(
        self,
        *,
        scheme_name: str,
        scheme: dict[str, Any],
    ) -> None:
        self.scheme_name = scheme_name
        self._scheme = dict(scheme)

    def openapi_security_scheme(self) -> dict[str, Any]:
        return dict(self._scheme)

    def openapi_security_requirement(self) -> dict[str, list[Any]]:
        return {self.scheme_name: []}

    def __call__(self, request: Any) -> None:
        return None


ADMIN_OPENAPI_SECURITY_DEPENDENCIES = (
    Security(
        AdminOpenAPISecurityDependency(
            scheme_name=ADMIN_HEADER_SCHEME,
            scheme=ADMIN_SECURITY_SCHEMES[ADMIN_HEADER_SCHEME],
        )
    ),
    Security(
        AdminOpenAPISecurityDependency(
            scheme_name=ADMIN_BEARER_SCHEME,
            scheme=ADMIN_SECURITY_SCHEMES[ADMIN_BEARER_SCHEME],
        )
    ),
)
logger = logging.getLogger(__name__)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _json_response(status: int, payload: dict[str, Any]) -> tuple[int, list[tuple[bytes, bytes]], bytes]:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode("ascii")),
    ]
    if status == 401:
        headers.append((b"www-authenticate", b"Bearer"))
    return status, headers, body


def _headers(scope: dict[str, Any]) -> dict[str, str]:
    return {
        key.decode("latin-1").lower(): value.decode("latin-1")
        for key, value in scope.get("headers", [])
    }


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
            "surface_rpc_enabled",
            "surface_diagnostics_enabled",
        )
    )


def _bootstrap_digest(settings_obj: object | None, enabled: bool) -> str | None:
    configured = os.environ.get(ADMIN_API_KEY_ENV) or getattr(settings_obj, "admin_api_key", None)
    if configured:
        return _digest(str(configured))
    if not enabled:
        return None

    key = secrets.token_urlsafe(32)
    digest = _digest(key)
    secret_dir = Path(str(getattr(settings_obj, "admin_api_key_dir", "runtime_secrets")))
    secret_dir.mkdir(parents=True, exist_ok=True)
    digest_path = secret_dir / "admin_api_key.sha256"
    digest_path.write_text(digest + "\n", encoding="utf-8")
    try:
        digest_path.chmod(0o600)
    except OSError:
        pass
    logger.warning(
        "Generated bootstrap admin API key for local control-plane surfaces. "
        "Set TIGRBL_AUTH_ADMIN_API_KEY to replace it. bootstrap_key=%s",
        key,
    )
    return digest


def _path_has_prefix(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


class AdminGate:
    """ASGI gate for generated local control-plane surfaces."""

    def __init__(
        self,
        app: Any,
        *,
        deployment: ResolvedDeployment,
        settings_obj: object | None = None,
        admin_path_prefixes: Iterable[str] = (),
        rpc_prefix: str = "/rpc",
        diagnostics_prefix: str = "/system",
    ) -> None:
        self.app = app
        self.deployment = deployment
        self.settings_obj = settings_obj
        self.admin_path_prefixes = tuple(dict.fromkeys(admin_path_prefixes))
        self.rpc_prefix = rpc_prefix
        self.diagnostics_prefix = diagnostics_prefix
        self.enabled = _control_plane_enabled(deployment)
        self._digest = _bootstrap_digest(settings_obj, self.enabled)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.app, name)

    def _requires_admin(self, path: str) -> bool:
        if not self.enabled:
            return False
        if self.deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(path, self.rpc_prefix):
            return True
        if self.deployment.flag_enabled("surface_diagnostics_enabled") and _path_has_prefix(path, self.diagnostics_prefix):
            return True
        if self.deployment.surface_enabled("admin-rpc"):
            return any(_path_has_prefix(path, prefix) for prefix in self.admin_path_prefixes)
        return False

    def _disabled_control_plane_path(self, path: str) -> bool:
        if not self.deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(path, self.rpc_prefix):
            return True
        if not self.deployment.flag_enabled("surface_diagnostics_enabled") and _path_has_prefix(path, self.diagnostics_prefix):
            return True
        return False

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        path = str(scope.get("path") or "")
        if self._disabled_control_plane_path(path):
            status, headers, body = _json_response(404, {"detail": "Not Found"})
            await send({"type": "http.response.start", "status": status, "headers": headers})
            await send({"type": "http.response.body", "body": body})
            return

        if self._requires_admin(path):
            credential = _extract_credential(scope)
            if not credential:
                status, headers, body = _json_response(401, {"error": "missing_admin_api_key"})
                await send({"type": "http.response.start", "status": status, "headers": headers})
                await send({"type": "http.response.body", "body": body})
                return
            if not self._digest or not hmac.compare_digest(_digest(credential), self._digest):
                status, headers, body = _json_response(403, {"error": "invalid_admin_api_key"})
                await send({"type": "http.response.start", "status": status, "headers": headers})
                await send({"type": "http.response.body", "body": body})
                return

        await self.app(scope, receive, send)


__all__ = [
    "ADMIN_SECURITY_REQUIREMENT",
    "ADMIN_SECURITY_SCHEMES",
    "AdminGate",
]
