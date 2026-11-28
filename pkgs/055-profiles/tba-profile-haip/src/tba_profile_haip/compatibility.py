"""HAIP revision compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class HaipCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool
    lossless: bool


COMPATIBILITY_PATHS = (
    HaipCompatibility(
        VERSION_HISTORY[0].identifier,
        CURRENT_VERSION.identifier,
        True,
        True,
        False,
    ),
    HaipCompatibility(
        CURRENT_VERSION.identifier,
        CURRENT_VERSION.identifier,
        True,
        False,
        True,
    ),
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> HaipCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return HaipCompatibility(source, target, False, False, False)


__all__ = ["COMPATIBILITY_PATHS", "HaipCompatibility", "compatibility"]
