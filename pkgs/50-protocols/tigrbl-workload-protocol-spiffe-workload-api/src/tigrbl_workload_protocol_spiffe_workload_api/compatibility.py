def require_version(identifier: str) -> None:
    if identifier != "SPIFFE-Workload-API-1.0": raise ValueError(f"unsupported Workload API revision: {identifier}")
