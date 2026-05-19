"""JWT Best Current Practices utilities for RFC 8725 compliance."""

from __future__ import annotations

import base64
import json
from typing import Any

from tigrbl_auth.config.settings import settings
from tigrbl_auth.errors import InvalidTokenError as BaseInvalidTokenError
from tigrbl_auth.services.token_service import JWTCoder


class InvalidTokenError(BaseInvalidTokenError):
    """Raised when a JWT violates RFC 8725 recommendations."""


RFC8725_SPEC_URL = "https://www.rfc-editor.org/rfc/rfc8725"


def validate_jwt_best_practices(
    token: str,
    *,
    enabled: bool | None = None,
) -> dict[str, Any]:
    if enabled is None:
        enabled = settings.enable_rfc8725
    claims = JWTCoder.default().decode(token)
    if not enabled:
        return claims
    head_b64 = token.split(".")[0]
    pad = "=" * ((4 - (len(head_b64) % 4)) % 4)
    header = json.loads(base64.urlsafe_b64decode(head_b64 + pad))
    if header.get("alg", "").lower() == "none":
        raise InvalidTokenError("alg 'none' is prohibited by RFC 8725")
    for required in ("iss", "aud", "exp", "sub"):
        if required not in claims:
            raise InvalidTokenError(f"missing '{required}' claim required by RFC 8725")
    return claims


__all__ = ["InvalidTokenError", "RFC8725_SPEC_URL", "validate_jwt_best_practices"]
