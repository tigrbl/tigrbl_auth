"""Deterministic RFC 8812 WebAuthn algorithm classification."""

from typing import Final, FrozenSet

RFC8812_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc8812"
WEBAUTHN_ALGORITHMS: Final[FrozenSet[str]] = frozenset(
    {
        "RS256",
        "RS384",
        "RS512",
        "RS1",
        "PS256",
        "PS384",
        "PS512",
        "ES256",
        "ES384",
        "ES512",
        "ES256K",
    }
)


def is_webauthn_algorithm(alg: object, *, enabled: bool = True) -> bool:
    if not enabled:
        return True
    return isinstance(alg, str) and alg.upper() in WEBAUTHN_ALGORITHMS


__all__ = ["RFC8812_SPEC_URL", "WEBAUTHN_ALGORITHMS", "is_webauthn_algorithm"]
