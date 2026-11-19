from .versions import CURRENT_VERSION


def migration_path(
    source: str, target: str = CURRENT_VERSION.identifier
) -> tuple[str, ...]:
    if source == target:
        return ()
    raise ValueError(f"manual WIT draft migration required: {source} to {target}")
