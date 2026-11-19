from dataclasses import dataclass

from .versions import CURRENT_VERSION, VcdmVersion


@dataclass(frozen=True, slots=True)
class VcdmCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


def compatibility(
    source: str, target: str = CURRENT_VERSION.value
) -> VcdmCompatibility:
    known = source in {version.value for version in VcdmVersion}
    return VcdmCompatibility(source, target, known, known and source != target)


__all__ = ["VcdmCompatibility", "compatibility"]
