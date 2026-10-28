def require_version(identifier: str) -> None:
    if identifier != "SPIFFE-v1.15.1-WIT-SVID":
        raise ValueError(f"unsupported WIT-SVID revision: {identifier}")
