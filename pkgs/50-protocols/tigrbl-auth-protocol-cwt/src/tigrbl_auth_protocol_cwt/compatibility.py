"""CWT revision compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION


@dataclass(frozen=True, slots=True)
class CwtCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


COMPATIBILITY_PATHS = (
    CwtCompatibility(CURRENT_VERSION.value, CURRENT_VERSION.value, True, False),
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.value,
) -> CwtCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return CwtCompatibility(source, target, False, False)


__all__ = ["COMPATIBILITY_PATHS", "CwtCompatibility", "compatibility"]
