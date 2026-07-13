from typing import Any, Mapping

REMOVED_GRANTS = frozenset({"implicit", "password"})


def migrate_client(
    value: Mapping[str, Any], *, source: str, target: str = "draft-ietf-oauth-v2-1-13"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source != "RFC6749" or target != "draft-ietf-oauth-v2-1-13":
        raise ValueError(f"unsupported OAuth migration: {source} -> {target}")
    grants = set(value.get("grant_types", ()))
    removed = grants & REMOVED_GRANTS
    if removed:
        raise ValueError(
            f"OAuth 2.1 migration requires replacement for removed grants: {sorted(removed)}"
        )
    migrated = dict(value)
    migrated["require_pkce"] = True
    return migrated


__all__ = ["REMOVED_GRANTS", "migrate_client"]
