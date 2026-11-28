"""Canonical security-event value contracts."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SecurityEventSubject:
    format: str
    identifiers: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class SecurityEvent:
    event_type: str
    issuer: str
    audience: tuple[str, ...]
    token_id: str
    issued_at: datetime
    subject: SecurityEventSubject | None = None
    data: Mapping[str, object] = field(default_factory=dict)


__all__ = ["SecurityEvent", "SecurityEventSubject"]
