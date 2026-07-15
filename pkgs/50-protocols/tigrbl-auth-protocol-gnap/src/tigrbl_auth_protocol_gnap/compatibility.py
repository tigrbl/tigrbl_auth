"""GNAP draft-to-RFC compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class GnapCompatibility:
    source: str
    target: str
    compatible: bool
    lossless: bool
    migration_required: bool


COMPATIBILITY_PATHS = tuple(
    GnapCompatibility(
        version.identifier,
        CURRENT_VERSION.identifier,
        True,
        True,
        version.identifier != CURRENT_VERSION.identifier,
    )
    for version in VERSION_HISTORY
)


def compatibility(
    source: str, target: str = CURRENT_VERSION.identifier
) -> GnapCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return GnapCompatibility(source, target, False, False, False)


__all__ = ["COMPATIBILITY_PATHS", "GnapCompatibility", "compatibility"]
