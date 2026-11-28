def migration_path(
    source: str, target: str = "SPIFFE-v1.15.1-WIT-SVID"
) -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(
        f"manual Incubating WIT-SVID migration required: {source} to {target}"
    )
