"""JWT revision compatibility paths."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION, VERSION_HISTORY


@dataclass(frozen=True, slots=True)
class JwtCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


COMPATIBILITY_PATHS = (
    JwtCompatibility(
        VERSION_HISTORY[0].identifier,
        CURRENT_VERSION.identifier,
        True,
        True,
    ),
    JwtCompatibility(
        CURRENT_VERSION.identifier,
        CURRENT_VERSION.identifier,
        True,
        False,
    ),
)


def compatibility(
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> JwtCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return JwtCompatibility(source, target, False, False)


__all__ = ["COMPATIBILITY_PATHS", "JwtCompatibility", "compatibility"]
