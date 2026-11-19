def migration_path(source: str, target: str = "RFC7515") -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"no automatic JWS migration from {source} to {target}")
