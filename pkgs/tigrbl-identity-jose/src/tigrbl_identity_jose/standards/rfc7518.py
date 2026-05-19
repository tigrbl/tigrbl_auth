"""RFC 7518 - JSON Web Algorithms (JWA).

Expose the list of algorithms supported by this service. When the Swarmauri JWA
registry is unavailable, a dependency-light fallback registry is used.
"""

from __future__ import annotations

from typing import Final

from tigrbl_auth.config.settings import settings

try:  # pragma: no cover - exercised when Swarmauri is installed
    from swarmauri_core.crypto.types import JWAAlg
    _BASE_ALGORITHMS = {alg.value for alg in JWAAlg}
except Exception:  # pragma: no cover - dependency-light checkpoint fallback
    _BASE_ALGORITHMS = {
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
        "PS256",
        "PS384",
        "PS512",
        "ES256",
        "ES384",
        "ES512",
        "EdDSA",
    }

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
    return sorted(algs)


__all__ = ["supported_algorithms", "RFC7518_SPEC_URL"]
