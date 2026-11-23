"""WebAuthn algorithm helpers for RFC 8812 compliance."""

from __future__ import annotations

from typing import Final, FrozenSet

from ..configuration import settings

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


def is_webauthn_algorithm(alg: object, *, enabled: bool | None = None) -> bool:
    if enabled is None:
        enabled = settings.enable_rfc8812
    if not enabled:
        return True
    if not isinstance(alg, str):
        return False
    return alg.upper() in WEBAUTHN_ALGORITHMS


__all__ = ["is_webauthn_algorithm", "WEBAUTHN_ALGORITHMS", "RFC8812_SPEC_URL"]
