"""Explicit Level 3 related-origin policy."""

from urllib.parse import urlsplit


def origin_is_allowed(
    origin: str, expected_origin: str, related_origins: tuple[str, ...] = ()
) -> bool:
    def normalized(value: str) -> str:
        parsed = urlsplit(value)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("related origins must be HTTPS origins")
        return f"https://{parsed.netloc}"

    supplied = normalized(origin)
    return supplied == normalized(expected_origin) or supplied in {
        normalized(value) for value in related_origins
    }


__all__ = ["origin_is_allowed"]
