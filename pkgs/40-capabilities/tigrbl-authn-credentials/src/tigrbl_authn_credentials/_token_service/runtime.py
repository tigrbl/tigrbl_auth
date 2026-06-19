from __future__ import annotations

import base64
import json
from datetime import timedelta
from typing import Any, Tuple

from tigrbl_identity_storage._persistence.sync_compat import _run as _run_coro

from ..key_management import _DEFAULT_KEY_PATH, _ensure_key, _provider


_ACCESS_TTL = timedelta(minutes=60)


_REFRESH_TTL = timedelta(days=7)


class RefreshTokenError(Exception):
    """Base class for refresh token lifecycle failures."""


class InvalidRefreshTokenError(RefreshTokenError):
    """The presented refresh token is invalid for the retained boundary."""


class RefreshTokenReuseError(RefreshTokenError):
    """A refresh token replay was detected and the family was revoked."""


def _load_runtime() -> dict[str, Any]:
    try:
        from tigrbl_identity_server.framework import ExportPolicy, FileKeyProvider, JWTTokenService, LocalKeyProvider, JWAAlg, KeyAlg, KeyClass, KeySpec, KeyUse
        from tigrbl_identity_runtime.settings import settings
        from tigrbl_auth_protocol_oauth.standards.mtls import validate_certificate_binding
        from tigrbl_auth_protocol_oauth.standards.revocation import is_revoked, is_revoked_async
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
