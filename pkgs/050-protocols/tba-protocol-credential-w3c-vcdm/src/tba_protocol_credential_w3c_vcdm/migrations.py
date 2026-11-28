from typing import Mapping

from .versions import VcdmVersion


def migrate_document(
    value: Mapping[str, object], *, source: str, target: str = "2.0"
) -> dict[str, object]:
    if source == target:
        return dict(value)
    if source != VcdmVersion.V1_1.value or target != VcdmVersion.V2_0.value:
        raise ValueError(f"unsupported VCDM migration: {source} -> {target}")
    migrated = dict(value)
    if "issuanceDate" in migrated and "validFrom" not in migrated:
        migrated["validFrom"] = migrated.pop("issuanceDate")
    return migrated


__all__ = ["migrate_document"]
