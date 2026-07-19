def migration_path(
    source: str, target: str = "draft-ietf-wimse-wpt-01"
) -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"manual WPT draft migration required: {source} to {target}")
