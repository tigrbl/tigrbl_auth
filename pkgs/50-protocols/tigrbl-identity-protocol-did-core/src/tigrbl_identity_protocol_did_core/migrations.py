def migration_path(source: str, target: str = "DID-Core-1.0") -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"no automatic DID Core migration from {source} to {target}")
