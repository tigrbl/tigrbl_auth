"""Conservative URI validation shared by identity protocols."""

from urllib.parse import urlsplit


def require_absolute_uri(value: str, *, https: bool = False) -> str:
    normalized = str(value).strip()
    parsed = urlsplit(normalized)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("absolute URI is required")
    if https and parsed.scheme.lower() != "https":
        raise ValueError("HTTPS URI is required")
    if parsed.fragment:
        raise ValueError("URI fragments are not permitted")
    return normalized


__all__ = ["require_absolute_uri"]
