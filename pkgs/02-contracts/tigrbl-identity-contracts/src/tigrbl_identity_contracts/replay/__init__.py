from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from .reservations import (
    ReplayKey,
    ReplayReservationPort,
    ReplayReservationRequest,
    ReplayReservationResult,
)


@dataclass(frozen=True, slots=True)
class PolicyReplayCase:
    case_id: str
    request: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.case_id:
            raise ValueError("case_id is required")
        object.__setattr__(self, "request", dict(self.request))


@dataclass(frozen=True, slots=True)
class PolicyReplayResult:
    case_id: str
    request_hash: str
    decision_hashes: tuple[str, ...]
    stable: bool
    decisions: tuple[Mapping[str, Any], ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class PolicyDeterminismReport:
    passed: bool
    policy_version: str
    schema_version: str
    results: tuple[PolicyReplayResult, ...]
    failures: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DecisionStabilityChange:
    case_id: str
    baseline_hash: str
    candidate_hash: str
    attributed: bool
    reason: str


@dataclass(frozen=True, slots=True)
class DecisionStabilityReport:
    passed: bool
    baseline_version: str
    candidate_version: str
    baseline_schema_version: str = ""
    candidate_schema_version: str = ""
    changes: tuple[DecisionStabilityChange, ...] = field(default_factory=tuple)
    failures: tuple[str, ...] = ()


PolicyEvaluator = Callable[[Mapping[str, Any]], Mapping[str, Any]]


__all__ = [
    "DecisionStabilityChange",
    "DecisionStabilityReport",
    "PolicyDeterminismReport",
    "PolicyReplayCase",
    "PolicyReplayResult",
    "PolicyEvaluator",
    "ReplayKey",
    "ReplayReservationPort",
    "ReplayReservationRequest",
    "ReplayReservationResult",
]
