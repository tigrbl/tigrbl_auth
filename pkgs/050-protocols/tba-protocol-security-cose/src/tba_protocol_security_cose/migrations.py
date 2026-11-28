def migration_path(source: str, target: str = "RFC9052") -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"no automatic COSE migration from {source} to {target}")
