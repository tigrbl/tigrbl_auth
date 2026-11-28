from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class DelegationStep:
    actor: str
    subject: str
    scopes: frozenset[str]
    proof_id: str


@dataclass(frozen=True)
class AuthorizationEvent:
    event_type: str
    subject_id: str
    actor_id: str
    decision: str
    correlation_id: str
    occurred_at: datetime
    attributes: Mapping[str, Any] = field(default_factory=dict)


__all__ = ["AuthorizationEvent", "DelegationStep"]
