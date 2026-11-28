from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CapabilityRecord:
    name: str
    enabled: bool
    evidence_id: str | None = None
    route: str | None = None


@dataclass
class AuthorizationState:
    subject_id: str
    version: int = 1
    updated_at: float = field(default_factory=time.time)
    mutations: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AuthorizationSnapshot:
    subject_id: str
    version: int
    issued_at: float
    max_staleness_seconds: int


__all__ = ["AuthorizationSnapshot", "AuthorizationState", "CapabilityRecord"]
