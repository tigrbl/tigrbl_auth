"""Supported EAT revision compatibility paths."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EatCompatibility:
    source: str
    target: str
    compatible: bool
    migration_required: bool


COMPATIBILITY_PATHS = (
    EatCompatibility("RFC9711", "RFC9711", True, False),
    EatCompatibility("draft-ietf-rats-eat-30", "RFC9711", True, True),
)


def compatibility(source: str, target: str = "RFC9711") -> EatCompatibility:
    for path in COMPATIBILITY_PATHS:
        if path.source == source and path.target == target:
            return path
    return EatCompatibility(source, target, False, False)


__all__ = ["COMPATIBILITY_PATHS", "EatCompatibility", "compatibility"]
