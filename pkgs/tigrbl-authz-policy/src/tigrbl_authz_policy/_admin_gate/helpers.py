from __future__ import annotations

import hashlib
import json
import os
import secrets
from pathlib import Path
from typing import Any, Awaitable, Callable

from tigrbl_identity_runtime.deployment import ResolvedDeployment

from .constants import ADMIN_API_KEY_ENV, ADMIN_API_KEY_HEADER, logger

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


def _platform_admin_raw_table_path(path: str, deployment: ResolvedDeployment) -> bool:
    if getattr(deployment, "product_surface", None) != "platform-admin-api":
        return False
    return _path_has_prefix(path, "/tenant") or _path_has_prefix(path, "/user")
