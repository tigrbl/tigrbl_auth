def migration_path(source: str, target: str = "RFC7516") -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"no automatic JWE migration from {source} to {target}")
