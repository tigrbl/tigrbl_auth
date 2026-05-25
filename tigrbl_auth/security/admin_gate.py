from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import secrets
from pathlib import Path
from typing import Any, Awaitable, Callable, Iterable

from tigrbl.security import APIKey, HTTPBearer, Security

from tigrbl_auth.config.deployment import ResolvedDeployment
from tigrbl_auth.services.admin_identity_bootstrap import (
    resolve_admin_user_from_request,
)

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


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _json_response(
    status: int, payload: dict[str, Any]
) -> tuple[int, list[tuple[bytes, bytes]], bytes]:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode("ascii")),
    ]
    if status == 401:
        headers.append((b"www-authenticate", b"Bearer"))
    return status, headers, body


async def _read_http_body(receive: Callable[[], Awaitable[dict[str, Any]]]) -> bytes:
    chunks: list[bytes] = []
    while True:
        message = await receive()
        if message.get("type") != "http.request":
            continue
        chunks.append(message.get("body", b""))
        if not message.get("more_body", False):
            break
    return b"".join(chunks)


def _replay_http_body(body: bytes) -> Callable[[], Awaitable[dict[str, Any]]]:
    sent = False

    async def receive() -> dict[str, Any]:
        nonlocal sent
        if sent:
            return {"type": "http.request", "body": b"", "more_body": False}
        sent = True
        return {"type": "http.request", "body": body, "more_body": False}

    return receive


def _jsonrpc_error(
    request_id: Any,
    code: int,
    message: str,
    data: Any | None = None,
) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


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
        if self.deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(
            path, self.rpc_prefix
        ):
            return True
        if self.deployment.flag_enabled(
            "surface_diagnostics_enabled"
        ) and _path_has_prefix(path, self.diagnostics_prefix):
            return True
        if self.deployment.surface_enabled("admin-rpc"):
            return any(
                _path_has_prefix(path, prefix) for prefix in self.admin_path_prefixes
            )
        return False

    def _disabled_control_plane_path(self, path: str) -> bool:
        if not self.deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(
            path, self.rpc_prefix
        ):
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
        if str(scope.get("method", "")).upper() != "POST":
            return False

        body = await _read_http_body(receive)
        try:
            payload = json.loads(body.decode("utf-8") or "null")
        except (UnicodeDecodeError, json.JSONDecodeError):
            status, headers, response_body = _json_response(
                200,
                _jsonrpc_error(None, -32700, "Parse error"),
            )
            await send(
                {"type": "http.response.start", "status": status, "headers": headers}
            )
            await send({"type": "http.response.body", "body": response_body})
            return True

        from tigrbl_auth.api.rpc import (
            RpcRequestContext,
            get_rpc_method,
            invoke_rpc_method_async,
        )

        async def handle_one(request: Any) -> dict[str, Any] | None:
            if not isinstance(request, dict):
                return _jsonrpc_error(None, -32600, "Invalid Request")
            request_id = request.get("id")
            method = request.get("method")
            if not isinstance(method, str):
                return _jsonrpc_error(request_id, -32600, "Invalid Request")
            try:
                get_rpc_method(method)
            except KeyError:
                return None
            if hasattr(
                self.deployment, "method_enabled"
            ) and not self.deployment.method_enabled(method):
                return _jsonrpc_error(request_id, -32601, "Method not found")
            try:
                context = RpcRequestContext(
                    repo_root=Path.cwd(),
                    deployment=self.deployment,
                    runtime_metadata={
                        "path": str(scope.get("path") or self.rpc_prefix)
                    },
                )
                result = await invoke_rpc_method_async(
                    method,
                    request.get("params") or {},
                    context=context,
                )
            except Exception as exc:  # pragma: no cover - surfaced through JSON-RPC
                return _jsonrpc_error(request_id, -32000, str(exc))
            return {"jsonrpc": "2.0", "id": request_id, "result": result}

        if isinstance(payload, list):
            responses: list[dict[str, Any]] = []
            unknown = False
            for item in payload:
                response = await handle_one(item)
                if response is None:
                    unknown = True
                    break
                responses.append(response)
            if unknown:
                await self.app(scope, _replay_http_body(body), send)
                return True
            status, headers, response_body = _json_response(
                200, {"responses": responses}
            )
            response_body = json.dumps(responses, separators=(",", ":")).encode("utf-8")
            headers = [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(response_body)).encode("ascii")),
            ]
            await send(
                {"type": "http.response.start", "status": status, "headers": headers}
            )
            await send({"type": "http.response.body", "body": response_body})
            return True

        response = await handle_one(payload)
        if response is None:
            await self.app(scope, _replay_http_body(body), send)
            return True
        status, headers, response_body = _json_response(200, response)
        await send(
            {"type": "http.response.start", "status": status, "headers": headers}
        )
        await send({"type": "http.response.body", "body": response_body})
        return True

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

        if self.deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(
            path, self.rpc_prefix
        ):
            if await self._dispatch_registry_rpc(scope, receive, send):
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
    "AdminGate",
]
