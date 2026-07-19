def require_version(identifier: str) -> None:
    if identifier != "DID-Core-1.0":
        raise ValueError(f"unsupported DID Core revision: {identifier}")