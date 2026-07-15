"""OID4VCI revision compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class Oid4vciCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


COMPATIBILITY_PATHS = tuple(
    Oid4vciCompatibility(
        version.identifier,
        CURRENT_VERSION.identifier,
        True,
        version.identifier != CURRENT_VERSION.identifier,
    )
    for version in VERSION_HISTORY
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> Oid4vciCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return Oid4vciCompatibility(source, target, False, False)


__all__ = ["COMPATIBILITY_PATHS", "Oid4vciCompatibility", "compatibility"]
