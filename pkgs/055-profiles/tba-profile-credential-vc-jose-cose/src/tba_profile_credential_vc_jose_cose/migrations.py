def migration_path(source: str, target: str = "VC-JOSE-COSE-1.0") -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"no automatic VC-JOSE-COSE migration from {source} to {target}")
