def validate_full_snapshot(
    previous: frozenset[str], current: frozenset[str], *, declared_full_snapshot: bool
) -> frozenset[str]:
    if not declared_full_snapshot:
        raise ValueError("SPIFFE stream updates must be complete snapshots")
    return current
