from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class XacmlDecision(StrEnum):
    PERMIT = "Permit"
    DENY = "Deny"
    NOT_APPLICABLE = "NotApplicable"
    INDETERMINATE = "Indeterminate"


@dataclass(frozen=True, slots=True)
class XacmlCategory:
    category_id: str
    attributes: Mapping[str, object]


__all__ = ["XacmlCategory", "XacmlDecision"]
