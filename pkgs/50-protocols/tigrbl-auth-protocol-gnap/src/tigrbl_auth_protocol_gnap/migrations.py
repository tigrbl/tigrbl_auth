from typing import Any, Mapping


def migrate_request(
    value: Mapping[str, Any], *, source: str, target: str = "RFC9635"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if (
        source not in {"draft-13", "draft-ietf-gnap-core-protocol-20"}
        or target != "RFC9635"
    ):
        raise ValueError(f"unsupported GNAP migration: {source} -> {target}")
    migrated = dict(value)
    migrated.setdefault("_migration", {})["from"] = source
    migrated["_migration"]["to"] = target
    return migrated


__all__ = ["migrate_request"]
