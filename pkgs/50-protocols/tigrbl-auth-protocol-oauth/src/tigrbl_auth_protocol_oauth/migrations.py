from typing import Any, Mapping

REMOVED_GRANTS = frozenset({"implicit", "password"})


def migrate_client(
    value: Mapping[str, Any],
    *,
    source: str,
    target: str = "draft-ietf-oauth-v2-1-15",
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    supported_drafts = {
        "draft-ietf-oauth-v2-1-13",
        "draft-ietf-oauth-v2-1-14",
        "draft-ietf-oauth-v2-1-15",
    }
    if target != "draft-ietf-oauth-v2-1-15" or source not in {
        "RFC6749",
        *supported_drafts,
    }:
        raise ValueError(f"unsupported OAuth migration: {source} -> {target}")
    if source in supported_drafts:
        return dict(value)
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
