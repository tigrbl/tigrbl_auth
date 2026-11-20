"""Versioned, deterministic verifiers for indexed API and service key lookup."""

from __future__ import annotations

import hashlib
import re

from .digests import sha256_digest

CREDENTIAL_DIGEST_V2_PREFIX = "v2$"
CREDENTIAL_DIGEST_LENGTH = len(CREDENTIAL_DIGEST_V2_PREFIX) + 64
_LEGACY_DIGEST = re.compile(r"[0-9a-f]{64}")
# Indexed equality lookup requires a stable public salt. This label separates
# the verifier from other uses of PBKDF2. Issued keys have 256 bits of entropy.
_LOOKUP_SALT = b"tba:durable-api-service-key:v2"
_ITERATIONS = 600_000


def harden_legacy_credential_digest(digest: str) -> str:
    """Upgrade a SHA-256 verifier without recovering the original credential."""
    if _LEGACY_DIGEST.fullmatch(digest) is None:
        raise ValueError("invalid legacy credential digest")
    derived = hashlib.pbkdf2_hmac(
        "sha256", bytes.fromhex(digest), _LOOKUP_SALT, _ITERATIONS
    )
    return CREDENTIAL_DIGEST_V2_PREFIX + derived.hex()


def text_credential_digest(value: str) -> str:
    """Use the text encoding and prehash that created the legacy records."""
    from .orm import KeyDigest

    if not value:
        raise ValueError("credential key is required")
    return harden_legacy_credential_digest(KeyDigest.digest_of(value))


def credential_digest(value: str | bytes) -> str:
    """Derive a stored verifier from text or opaque binary key material."""
    if isinstance(value, str):
        return text_credential_digest(value)
    if not value:
        raise ValueError("credential key is required")
    # Opaque bytes can be used by standalone providers. HTTP key entry
    # points use the existing text format and its canonical prehash.
    return harden_legacy_credential_digest(sha256_digest(bytes(value)).hex())
