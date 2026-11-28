"""Policy decision contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass

from .kinds import PolicyKind


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason: str
    matched: tuple[str, ...] = ()
    trace_id: str = ""


@dataclass(frozen=True, slots=True)
class PolicyTrace:
    trace_id: str
    subject: str
    tenant_id: str
    action: str
    allowed: bool
    reason: str
    matched: tuple[str, ...]
    evaluated_kinds: tuple[PolicyKind, ...]
    recorded_at: str


__all__ = ["PolicyDecision", "PolicyTrace"]
