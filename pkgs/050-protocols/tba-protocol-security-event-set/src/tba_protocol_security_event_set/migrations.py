from typing import Any, Mapping


def migrate_claims(
    value: Mapping[str, Any], *, source: str, target: str = "RFC8417"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source != "draft-ietf-secevent-token-13" or target != "RFC8417":
        raise ValueError(f"unsupported SET migration: {source} -> {target}")
    migrated = dict(value)
    if "events" not in migrated:
        raise ValueError("SET migration requires the events claim")
    return migrated


__all__ = ["migrate_claims"]
