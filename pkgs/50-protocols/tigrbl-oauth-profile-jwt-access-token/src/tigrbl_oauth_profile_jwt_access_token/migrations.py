def migration_path(source: str, target: str = "RFC9068") -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"no automatic profile migration from {source} to {target}")
