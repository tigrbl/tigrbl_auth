"""Configuration migration for RP composite profiles."""

from typing import Any, Mapping

from .versions import CURRENT_VERSION, VERSION_HISTORY


def migrate_configuration(
    value: Mapping[str, Any],
    *,
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source != VERSION_HISTORY[0].identifier or target != CURRENT_VERSION.identifier:
        raise ValueError(f"unsupported RP profile migration: {source} -> {target}")
    migrated = dict(value)
    migrated["pkce_method"] = "S256"
    migrated["browser_storage_policy"] = "memory_only"
    return migrated


__all__ = ["migrate_configuration"]
