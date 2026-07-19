def migration_path(source: str, target: str = "draft-ietf-wimse-workload-creds-02") -> tuple[str, ...]:
    if source == target: return ()
    raise ValueError(f"manual WIT draft migration required: {source} to {target}")
