"""JWK Thumbprint utilities for RFC 7638 compliance."""

from __future__ import annotations

import base64
import json
from hashlib import sha256
from typing import Any, Final, Mapping

from tigrbl_auth.config.settings import settings

RFC7638_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7638"
_REQUIRED_MEMBERS: dict[str, tuple[str, ...]] = {
    "RSA": ("e", "kty", "n"),
    "EC": ("crv", "kty", "x", "y"),
    "OKP": ("crv", "kty", "x"),
    "oct": ("k", "kty"),
}


def jwk_thumbprint(jwk: Mapping[str, Any], *, enabled: bool | None = None) -> str:
    if enabled is None:
        enabled = settings.enable_rfc7638
    if not enabled:
        return ""
    kty = jwk.get("kty")
    members = _REQUIRED_MEMBERS.get(kty)
    if not members:
        raise ValueError(f"unsupported kty: {kty}")
    obj = {key: jwk[key] for key in members}
    canonical = json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")
    digest = sha256(canonical).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def verify_jwk_thumbprint(
    jwk: Mapping[str, Any],
    thumbprint: str,
    *,
    enabled: bool | None = None,
) -> bool:
    if enabled is None:
        enabled = settings.enable_rfc7638
    if not enabled:
        return True
    try:
        expected = jwk_thumbprint(jwk, enabled=True)
    except Exception:
        return False
    return expected == thumbprint


__all__ = ["RFC7638_SPEC_URL", "jwk_thumbprint", "verify_jwk_thumbprint"]
