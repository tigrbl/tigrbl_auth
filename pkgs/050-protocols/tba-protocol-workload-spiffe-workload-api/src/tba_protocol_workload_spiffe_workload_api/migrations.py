def migration_path(
    source: str, target: str = "SPIFFE-Workload-API-1.0"
) -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"manual Workload API migration required: {source} to {target}")
