"""OID4VP revision compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class Oid4vpCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool
    lossless: bool


COMPATIBILITY_PATHS = (
    Oid4vpCompatibility(
        VERSION_HISTORY[0].identifier,
        CURRENT_VERSION.identifier,
        True,
        True,
        False,
    ),
    Oid4vpCompatibility(
        VERSION_HISTORY[1].identifier,
        CURRENT_VERSION.identifier,
        True,
        True,
        True,
    ),
    Oid4vpCompatibility(
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
) -> Oid4vpCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return Oid4vpCompatibility(source, target, False, False, False)


__all__ = ["COMPATIBILITY_PATHS", "Oid4vpCompatibility", "compatibility"]
