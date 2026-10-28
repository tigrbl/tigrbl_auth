def migration_path(
    source: str, target: str = "TIGRBL-CWT-SVID-EXPERIMENT-1"
) -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(
        f"no automatic experimental CWT-SVID migration from {source} to {target}"
    )
