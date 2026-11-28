from dataclasses import dataclass

from .versions import CURRENT_VERSION


@dataclass(frozen=True, slots=True)
class IsoMdocCompatibility:
    source: str
    target: str
    compatible: bool


def compatibility(
    source: str, target: str = CURRENT_VERSION.value
) -> IsoMdocCompatibility:
    return IsoMdocCompatibility(
        source, target, source == target == CURRENT_VERSION.value
    )


__all__ = ["IsoMdocCompatibility", "compatibility"]
