"""Proof Key for Code Exchange utilities.

This module keeps the OAuth protocol public API while delegating reusable
RFC 7636 proof-key primitives to ``tigrbl-security-proof-pkce``.

See RFC 7636: https://www.rfc-editor.org/rfc/rfc7636
"""

from __future__ import annotations

import warnings
from typing import Final

from tigrbl_security_proof_pkce import (
    PKCE_SPEC_URL,
    make_pkce_verifier,
    pkce_s256_challenge,
    validate_pkce_verifier,
    verify_pkce_s256_challenge,
)
from tigrbl_identity_contracts.protocol_configuration import (
    protocol_settings as settings,
)

RFC7636_SPEC_URL: Final = PKCE_SPEC_URL


def makeCodeVerifier(length: int = 43) -> str:
    """Return a high-entropy RFC 7636 ``code_verifier`` string."""

    try:
        return make_pkce_verifier(length)
    except ValueError as exc:
        raise ValueError("length must be between 43 and 128 characters") from exc


def makeCodeChallenge(verifier: str) -> str:
    """Derive an ``S256`` ``code_challenge`` from *verifier*."""

    try:
        value = validate_pkce_verifier(verifier)
    except ValueError as exc:
        raise ValueError("invalid code_verifier") from exc
    return pkce_s256_challenge(value)


def verify_code_challenge(
    verifier: str, challenge: str, *, enabled: bool | None = None
) -> bool:
    """Return ``True`` if *challenge* matches *verifier* using ``S256``."""

    if enabled is None:
        enabled = settings.enable_rfc7636
    return verify_pkce_s256_challenge(verifier, challenge, enabled=enabled)


def create_code_verifier(length: int = 43) -> str:
    warnings.warn(
        "create_code_verifier is deprecated, use makeCodeVerifier",
        DeprecationWarning,
        stacklevel=2,
    )
    return makeCodeVerifier(length)


def create_code_challenge(verifier: str) -> str:
    warnings.warn(
        "create_code_challenge is deprecated, use makeCodeChallenge",
        DeprecationWarning,
        stacklevel=2,
    )
    return makeCodeChallenge(verifier)


__all__ = [
    "makeCodeVerifier",
    "makeCodeChallenge",
    "verify_code_challenge",
    "RFC7636_SPEC_URL",
    "create_code_verifier",
    "create_code_challenge",
]
