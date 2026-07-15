"""Compatibility paths for the OAuth authorization-framework profile."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class OAuthCompatibility:
    source: str
    target: str
    compatible: bool
    lossless: bool
    migration_required: bool


COMPATIBILITY_PATHS = tuple(
    OAuthCompatibility(
        source=version.identifier,
        target=CURRENT_VERSION.identifier,
        compatible=True,
        lossless=version.identifier == CURRENT_VERSION.identifier,
        migration_required=version.identifier != CURRENT_VERSION.identifier,
    )
    for version in VERSION_HISTORY
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> OAuthCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return OAuthCompatibility(source, target, False, False, False)


__all__ = ["COMPATIBILITY_PATHS", "OAuthCompatibility", "compatibility"]
