def require_version(identifier: str) -> None:
    if identifier != "draft-ietf-wimse-workload-creds-02":
        raise ValueError(f"unsupported WIT draft: {identifier}")
