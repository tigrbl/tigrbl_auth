"""Compatibility paths into the versioned protected-resource profile."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION


@dataclass(frozen=True, slots=True)
class ProtectedResourceCompatibility:
    source: str
    target: str
    compatible: bool
    lossless: bool
    migration_required: bool


COMPATIBILITY_PATHS = (
    ProtectedResourceCompatibility(
        "legacy-unversioned",
        CURRENT_VERSION.identifier,
        True,
        True,
        True,
    ),
    ProtectedResourceCompatibility(
        CURRENT_VERSION.identifier,
        CURRENT_VERSION.identifier,
        True,
        True,
        False,
    ),
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> ProtectedResourceCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return ProtectedResourceCompatibility(source, target, False, False, False)


__all__ = [
    "COMPATIBILITY_PATHS",
    "ProtectedResourceCompatibility",
    "compatibility",
]
