from __future__ import annotations

import hmac
import json
from pathlib import Path
from typing import Any, Awaitable, Callable, Iterable

from tigrbl_identity_runtime.deployment import ResolvedDeployment
from tigrbl_auth.services.admin_identity_bootstrap import resolve_admin_user_from_request

from .helpers import (
    _bootstrap_digest,
    _control_plane_enabled,
    _digest,
    _extract_credential,
    _json_response,
    _jsonrpc_error,
    _path_has_prefix,
    _platform_admin_raw_table_path,
    _read_http_body,
    _replay_http_body,
)

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
        openrpc_path: str = "/openrpc.json",
        diagnostics_prefix: str = "/system",
    ) -> None:
        self.app = app
        self.deployment = deployment
        self.settings_obj = settings_obj
        self.admin_path_prefixes = tuple(dict.fromkeys(admin_path_prefixes))
        self.rpc_prefix = rpc_prefix
        self.openrpc_path = openrpc_path
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
        if self.deployment.flag_enabled("surface_admin_enabled"):
            return any(
                _path_has_prefix(path, prefix) for prefix in self.admin_path_prefixes
            )
        return False

    def _disabled_control_plane_path(self, path: str) -> bool:
        if _platform_admin_raw_table_path(path, self.deployment):
            return True
        if not self.deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(
            path, self.rpc_prefix
        ):
            return True
        if not self.deployment.flag_enabled("surface_rpc_enabled") and path == self.openrpc_path:
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
