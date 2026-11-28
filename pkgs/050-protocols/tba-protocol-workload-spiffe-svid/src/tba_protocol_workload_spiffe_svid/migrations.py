def migration_path(source: str, target: str = "SPIFFE-1.0") -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"no automatic SPIFFE SVID migration from {source} to {target}")
