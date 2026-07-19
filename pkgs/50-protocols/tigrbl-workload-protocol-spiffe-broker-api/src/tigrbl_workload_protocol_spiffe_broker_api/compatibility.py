def require_version(identifier: str) -> None:
    if identifier != "SPIFFE-v1.15.1-Broker-API": raise ValueError(f"unsupported Broker API revision: {identifier}")
