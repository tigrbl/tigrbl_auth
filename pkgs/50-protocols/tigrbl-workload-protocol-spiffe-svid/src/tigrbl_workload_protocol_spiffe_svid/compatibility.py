def require_version(identifier: str) -> None:
    if identifier != "SPIFFE-1.0": raise ValueError(f"unsupported SPIFFE SVID revision: {identifier}")
