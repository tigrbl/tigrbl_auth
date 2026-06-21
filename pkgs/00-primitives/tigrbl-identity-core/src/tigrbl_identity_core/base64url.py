"""Base64url helpers shared by identity packages."""

from __future__ import annotations

import base64


def base64url_encode(data: bytes | bytearray | memoryview) -> str:
    """Return unpadded base64url text for byte-oriented data."""

    return base64.urlsafe_b64encode(bytes(data)).rstrip(b"=").decode("ascii")


def base64url_decode(value: str) -> bytes:
    """Decode unpadded base64url text into bytes."""

    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


__all__ = ["base64url_decode", "base64url_encode"]
