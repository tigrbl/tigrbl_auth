"""RP composite-profile compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class RpCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


COMPATIBILITY_PATHS = (
    RpCompatibility(
        VERSION_HISTORY[0].identifier,
        CURRENT_VERSION.identifier,
        True,
        True,
    ),
    RpCompatibility(
        CURRENT_VERSION.identifier,
        CURRENT_VERSION.identifier,
        True,
        False,
    ),
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> RpCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return RpCompatibility(source, target, False, False)


__all__ = ["COMPATIBILITY_PATHS", "RpCompatibility", "compatibility"]
