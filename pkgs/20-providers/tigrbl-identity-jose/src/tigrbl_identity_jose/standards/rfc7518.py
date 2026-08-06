"""RFC 7518 - JSON Web Algorithms (JWA).

Expose the algorithms implemented by Tigrbl Auth's JOSE runtime.
"""

from __future__ import annotations

from typing import Final

from ..pqc import ML_DSA_65_ALG
from ..configuration import settings

_BASE_ALGORITHMS = {"HS256", "RS256", "EdDSA"}

RFC7518_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc7518"
WEBAUTHN_ALGORITHMS = frozenset({"RS256", "RS384", "RS512", "RS1", "PS256", "PS384", "PS512", "ES256", "ES384", "ES512", "ES256K"})


def supported_algorithms() -> list[str]:
    """Return algorithms supported for JOSE operations."""
    if not settings.enable_rfc7518:
        raise RuntimeError(f"RFC 7518 support disabled: {RFC7518_SPEC_URL}")

    algs = set(_BASE_ALGORITHMS)
    if settings.enable_rfc8812:
        algs.update(WEBAUTHN_ALGORITHMS)
    else:
        algs.difference_update(WEBAUTHN_ALGORITHMS)
        algs.add("RS256")
    if getattr(settings, "enable_pqc_jose", False) or str(getattr(settings, "jwt_signing_alg", "")) == ML_DSA_65_ALG:
        algs.add(ML_DSA_65_ALG)
    return sorted(algs)


__all__ = ["supported_algorithms", "RFC7518_SPEC_URL"]
