from __future__ import annotations

import base64
import json
from typing import Any, Tuple

from tigrbl_identity_contracts.tokens import (
    DEFAULT_ACCESS_TOKEN_TTL,
    DEFAULT_REFRESH_TOKEN_TTL,
)
from tigrbl_identity_storage.tables._sync import run_async as _run_coro

from .key_management import _DEFAULT_KEY_PATH, _ensure_key, _provider


_ACCESS_TTL = DEFAULT_ACCESS_TOKEN_TTL
_REFRESH_TTL = DEFAULT_REFRESH_TOKEN_TTL


def _load_runtime() -> dict[str, Any]:
    try:
        from swarmauri_core.crypto.types import ExportPolicy, JWAAlg, KeyUse
        from swarmauri_core.key_providers.types import KeyAlg, KeyClass, KeySpec
        from swarmauri_keyprovider_file import FileKeyProvider
        from swarmauri_keyprovider_local import LocalKeyProvider
        from swarmauri_tokens_jwt import JWTTokenService
        from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import validate_certificate_binding
        from tigrbl_auth_protocol_oauth.standards.revocation import is_revoked, is_revoked_async
        from tigrbl_identity_runtime.settings import settings
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("runtime token-service dependencies are unavailable") from exc
    return {
        "ExportPolicy": ExportPolicy,
        "FileKeyProvider": FileKeyProvider,
        "JWTTokenService": JWTTokenService,
        "LocalKeyProvider": LocalKeyProvider,
        "JWAAlg": JWAAlg,
        "KeyAlg": KeyAlg,
        "KeyClass": KeyClass,
        "KeySpec": KeySpec,
        "KeyUse": KeyUse,
        "settings": settings,
        "validate_certificate_binding": validate_certificate_binding,
        "is_revoked": is_revoked,
        "is_revoked_async": is_revoked_async,
    }


def _run(coro):
    return _run_coro(coro)


def _svc() -> Tuple[Any, str]:
    runtime = _load_runtime()
    kp = _provider()
    if _DEFAULT_KEY_PATH.exists():
        kid = _DEFAULT_KEY_PATH.read_text().strip()
        if kid:
            try:
                _run(kp.get_key(kid, include_secret=False))
            except Exception:
                kid, _, _ = _run(_ensure_key())
        else:
            kid, _, _ = _run(_ensure_key())
    else:
        spec = runtime["KeySpec"](
            klass=runtime["KeyClass"].asymmetric,
            alg=runtime["KeyAlg"].ED25519,
            uses=(runtime["KeyUse"].SIGN, runtime["KeyUse"].VERIFY),
            export_policy=runtime["ExportPolicy"].SECRET_WHEN_ALLOWED,
            label="jwt_ed25519",
        )
        ref = _run(kp.create_key(spec))
        kid = ref.kid
        _DEFAULT_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        _DEFAULT_KEY_PATH.write_text(kid)
    service = runtime["JWTTokenService"](kp)
    return service, kid


async def _svc_async() -> Tuple[Any, str]:
    runtime = _load_runtime()
    kp = _provider()
    if _DEFAULT_KEY_PATH.exists():
        kid = _DEFAULT_KEY_PATH.read_text().strip()
        if kid:
            try:
                await kp.get_key(kid, include_secret=False)
            except Exception:
                kid, _, _ = await _ensure_key()
        else:
            kid, _, _ = await _ensure_key()
    else:
        spec = runtime["KeySpec"](
            klass=runtime["KeyClass"].asymmetric,
            alg=runtime["KeyAlg"].ED25519,
            uses=(runtime["KeyUse"].SIGN, runtime["KeyUse"].VERIFY),
            export_policy=runtime["ExportPolicy"].SECRET_WHEN_ALLOWED,
            label="jwt_ed25519",
        )
        ref = await kp.create_key(spec)
        kid = ref.kid
        _DEFAULT_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        _DEFAULT_KEY_PATH.write_text(kid)
    service = runtime["JWTTokenService"](kp)
    return service, kid


def _header_alg(token: str) -> str:
    try:
        header_segment = token.split(".")[0]
        padded = header_segment + "=" * (-len(header_segment) % 4)
        header = json.loads(base64.urlsafe_b64decode(padded).decode())
        return str(header.get("alg", "")).lower()
    except Exception:
        return ""


__all__ = [
    "_ACCESS_TTL",
    "_REFRESH_TTL",
    "_header_alg",
    "_load_runtime",
    "_run",
    "_svc",
    "_svc_async",
]
