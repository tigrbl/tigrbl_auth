from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping, Sequence


class XacmlDecisionValue(StrEnum):
    PERMIT = "Permit"
    DENY = "Deny"
    NOT_APPLICABLE = "NotApplicable"
    INDETERMINATE = "Indeterminate"


@dataclass(frozen=True, slots=True)
class XacmlCategory:
    category_id: str
    attributes: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class XacmlDecisionResult:
    decision: XacmlDecisionValue
    status: Mapping[str, object] = field(default_factory=dict)
    obligations: Sequence[Mapping[str, object]] = ()
    advice: Sequence[Mapping[str, object]] = ()


# Compatibility name for callers that imported the value enum.
XacmlDecision = XacmlDecisionValue


__all__ = [
    "XacmlCategory",
    "XacmlDecision",
    "XacmlDecisionResult",
    "XacmlDecisionValue",
]
