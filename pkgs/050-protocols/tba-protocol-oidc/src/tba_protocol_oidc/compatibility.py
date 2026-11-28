"""OIDC Core revision compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION


@dataclass(frozen=True, slots=True)
class OidcCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


COMPATIBILITY_PATHS = (
    OidcCompatibility("1.0", CURRENT_VERSION.identifier, True, True),
    OidcCompatibility(
        CURRENT_VERSION.identifier,
        CURRENT_VERSION.identifier,
        True,
        False,
    ),
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> OidcCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return OidcCompatibility(source, target, False, False)


__all__ = ["COMPATIBILITY_PATHS", "OidcCompatibility", "compatibility"]
