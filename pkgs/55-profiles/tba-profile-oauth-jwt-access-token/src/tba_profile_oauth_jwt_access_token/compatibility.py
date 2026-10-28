def require_version(identifier: str) -> None:
    if identifier != "RFC9068":
        raise ValueError(f"unsupported JWT access-token profile: {identifier}")
