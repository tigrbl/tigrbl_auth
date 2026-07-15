def migration_path(source: str, target: str) -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(
        f"unsupported FIDO2 server profile migration: {source} -> {target}"
    )


__all__ = ["migration_path"]
