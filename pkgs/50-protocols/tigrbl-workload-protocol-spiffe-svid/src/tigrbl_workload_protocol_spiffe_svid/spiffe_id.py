from urllib.parse import urlsplit

def validate_spiffe_id(value: str) -> tuple[str, str]:
    parsed = urlsplit(value)
    if parsed.scheme != "spiffe" or not parsed.netloc or parsed.query or parsed.fragment or parsed.username or parsed.password or parsed.port:
        raise ValueError("invalid SPIFFE ID")
    if parsed.path == "/" or "//" in parsed.path or parsed.path.endswith("/"):
        raise ValueError("non-canonical SPIFFE ID path")
    if len(value) > 2048:
        raise ValueError("SPIFFE ID exceeds maximum length")
    return parsed.netloc, parsed.path