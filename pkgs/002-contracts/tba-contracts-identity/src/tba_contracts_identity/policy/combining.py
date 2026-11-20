"""Policy combining-algorithm contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from .decisions import PolicyDecision


class CombiningAlgorithmKind(str, Enum):
    DENY_OVERRIDES = "deny_overrides"
    PERMIT_OVERRIDES = "permit_overrides"
    FIRST_APPLICABLE = "first_applicable"
    ONLY_ONE_APPLICABLE = "only_one_applicable"


@dataclass(frozen=True, slots=True)
class PolicyCombineRequest:
    decisions: tuple[PolicyDecision, ...]
    algorithm: CombiningAlgorithmKind = CombiningAlgorithmKind.DENY_OVERRIDES


class PolicyCombinerPort(Protocol):
    def combine(self, request: PolicyCombineRequest, /) -> PolicyDecision: ...


__all__ = ["CombiningAlgorithmKind", "PolicyCombineRequest", "PolicyCombinerPort"]
