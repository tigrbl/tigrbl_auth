def migration_path(source: str, target: str = "SPIFFE-v1.15.1-Broker-API") -> tuple[str, ...]:
    if source == target: return ()
    raise ValueError(f"manual Incubating Broker API migration required: {source} to {target}")
