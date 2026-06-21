"""Digest helpers shared by identity packages."""

from __future__ import annotations

import hashlib


def sha256_text_digest(value: str) -> str:
    """Return the SHA-256 hex digest of UTF-8 text."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


__all__ = ["sha256_text_digest"]
