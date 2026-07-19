def require_version(identifier: str) -> None:
    if identifier != "VC-JOSE-COSE-1.0": raise ValueError(f"unsupported VC-JOSE-COSE revision: {identifier}")
