"""SD-JWT VC draft compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class SdJwtVcCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


COMPATIBILITY_PATHS = tuple(
    SdJwtVcCompatibility(
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
) -> SdJwtVcCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return SdJwtVcCompatibility(source, target, False, False)


__all__ = ["COMPATIBILITY_PATHS", "SdJwtVcCompatibility", "compatibility"]
