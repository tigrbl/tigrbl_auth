"""Deterministic configuration migration between JOSE suite revisions."""

from collections.abc import Mapping

from .errors import UnsupportedJoseMigrationError
from .versions import CURRENT_VERSION, VERSION_HISTORY


def migrate_configuration(
    value: Mapping[str, object],
    *,
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> dict[str, object]:
    if source == target:
        return dict(value)
    if source == VERSION_HISTORY[0].identifier and target == CURRENT_VERSION.identifier:
        migrated = dict(value)
        migrated.setdefault("require_explicit_algorithm_allowlist", True)
        migrated.setdefault("reject_unsafe_jwt_types", True)
        return migrated
    raise UnsupportedJoseMigrationError(
        f"unsupported JOSE suite migration: {source} -> {target}"
    )


__all__ = ["migrate_configuration"]
