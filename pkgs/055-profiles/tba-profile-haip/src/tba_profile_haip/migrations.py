from typing import Any, Mapping


def migrate_configuration(
    value: Mapping[str, Any], *, source: str, target: str = "1.0"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source != "draft-03" or target != "1.0":
        raise ValueError(f"unsupported HAIP migration: {source} -> {target}")
    migrated = dict(value)
    if "presentation_definition" in migrated:
        raise ValueError(
            "HAIP draft Presentation Exchange constraints require an explicit DCQL migration"
        )
    migrated["oid4vci_version"] = "1.0"
    migrated["oid4vp_version"] = "1.0"
    return migrated


__all__ = ["migrate_configuration"]
