from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


class InvariantSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class VerificationMethod(str, Enum):
    STATIC = "static"
    RUNTIME = "runtime"
    REPLAY = "replay"
    GRAPH = "graph"
    MANUAL = "manual"


def _stable_tuple(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if str(value)}))


@dataclass(frozen=True, slots=True)
class AuthorizationInvariant:
    invariant_id: str
    title: str
    property_family: str
    statement: str
    verification_method: VerificationMethod
    severity: InvariantSeverity = InvariantSeverity.ERROR
    enabled: bool = True
    feature_ids: tuple[str, ...] = ()
    spec_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.invariant_id:
            raise ValueError("invariant_id is required")
        if not self.title:
            raise ValueError("title is required")
        if not self.property_family:
            raise ValueError("property_family is required")
        if not self.statement:
            raise ValueError("statement is required")
        object.__setattr__(self, "verification_method", VerificationMethod(self.verification_method))
        object.__setattr__(self, "severity", InvariantSeverity(self.severity))
        object.__setattr__(self, "feature_ids", _stable_tuple(self.feature_ids))
        object.__setattr__(self, "spec_ids", _stable_tuple(self.spec_ids))
        object.__setattr__(self, "tags", _stable_tuple(self.tags))


@dataclass(frozen=True, slots=True)
class InvariantEvaluation:
    invariant_id: str
    passed: bool
    message: str
    evaluated_at: str
    evidence: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class InvariantViolation:
    invariant_id: str
    severity: InvariantSeverity
    message: str
    evidence: Mapping[str, Any] = field(default_factory=dict)


__all__ = [
    "AuthorizationInvariant",
    "InvariantEvaluation",
    "InvariantSeverity",
    "InvariantViolation",
    "VerificationMethod",
]
