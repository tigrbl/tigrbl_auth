"""RFC 7519 - JSON Web Token (JWT).

The canonical helpers prefer the runtime ``JWTCoder`` implementation, but they
also provide a dependency-light HS256 fallback for checkpoint environments where
Tigrbl/Swarmauri runtime services are not importable.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any, Final

try:
    import jwt as pyjwt
except ModuleNotFoundError:  # pragma: no cover - dependency-light fallback
    pyjwt = None

from tigrbl_auth.config.settings import settings
from tigrbl_auth.errors import InvalidTokenError
from tigrbl_auth.services.token_service import JWTCoder

RFC7519_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7519"
_FALLBACK_ALGORITHM: Final[str] = "HS256"


def _runtime_coder() -> JWTCoder | None:
    try:
        return JWTCoder.default()
    except Exception:
        return None


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def _secret_bytes() -> bytes:
    secret = getattr(settings, "jwt_secret", "")
    return secret.encode("utf-8") if isinstance(secret, str) else bytes(secret)


def _fallback_encode(**claims: Any) -> str:
    if pyjwt is not None:
        return str(pyjwt.encode(claims, settings.jwt_secret, algorithm=_FALLBACK_ALGORITHM))
    header = {"alg": _FALLBACK_ALGORITHM, "typ": "JWT"}
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    payload_b64 = _b64url_encode(json.dumps(claims, separators=(",", ":"), sort_keys=True, default=str).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(_secret_bytes(), signing_input, hashlib.sha256).digest()
    return f"{header_b64}.{payload_b64}.{_b64url_encode(signature)}"


def _fallback_decode(token: str) -> dict[str, Any]:
    try:
        if pyjwt is not None:
            payload = pyjwt.decode_complete(token, options={"verify_signature": False}).get("payload", {})
            options = {"require": ["exp"]} if "exp" in payload else {}
            decode_options = {"verify_aud": False}
            decode_options.update(options)
            return dict(pyjwt.decode(token, settings.jwt_secret, algorithms=[_FALLBACK_ALGORITHM], options=decode_options))
        parts = token.split(".")
        if len(parts) != 3:
            raise InvalidTokenError("malformed token")
        header_b64, payload_b64, signature_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected = hmac.new(_secret_bytes(), signing_input, hashlib.sha256).digest()
        actual = _b64url_decode(signature_b64)
        if not hmac.compare_digest(expected, actual):
            raise InvalidTokenError("unable to verify token")
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
        if "exp" in payload and int(payload["exp"]) < int(time.time()):
            raise InvalidTokenError("unable to verify token")
        return dict(payload)
    except InvalidTokenError:
        raise
    except Exception as exc:
        raise InvalidTokenError("unable to verify token") from exc


def encode_jwt(**claims: Any) -> str:
    """Encode *claims* as a JWT string."""
    if not settings.enable_rfc7519:
        raise RuntimeError(f"RFC 7519 support disabled: {RFC7519_SPEC_URL}")
    sub = claims.pop("sub", "")
    coder = _runtime_coder()
    if coder is not None:
        return coder.sign(sub=sub, **claims)
    return _fallback_encode(sub=sub, **claims)


def decode_jwt(token: str) -> dict[str, Any]:
    """Decode and verify *token* returning the claims dictionary."""
    if not settings.enable_rfc7519:
        raise RuntimeError(f"RFC 7519 support disabled: {RFC7519_SPEC_URL}")
    coder = _runtime_coder()
    if coder is not None:
        return coder.decode(token)
    return _fallback_decode(token)


__all__ = ["encode_jwt", "decode_jwt", "RFC7519_SPEC_URL"]
