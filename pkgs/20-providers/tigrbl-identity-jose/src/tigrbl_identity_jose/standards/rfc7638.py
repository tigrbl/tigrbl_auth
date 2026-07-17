"""JWK Thumbprint utilities for RFC 7638 compliance."""

from __future__ import annotations

from typing import Any, Final, Mapping

from tigrbl_jose_concrete import jwk_thumbprint as _jwk_thumbprint
from tigrbl_jose_concrete import verify_jwk_thumbprint as _verify_jwk_thumbprint
from ..configuration import settings

RFC7638_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7638"


def jwk_thumbprint(jwk: Mapping[str, Any], *, enabled: bool | None = None) -> str:
    if enabled is None:
        enabled = settings.enable_rfc7638
    if not enabled:
        return ""
    return _jwk_thumbprint(jwk)


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
    return _verify_jwk_thumbprint(jwk, thumbprint)


__all__ = ["RFC7638_SPEC_URL", "jwk_thumbprint", "verify_jwk_thumbprint"]
