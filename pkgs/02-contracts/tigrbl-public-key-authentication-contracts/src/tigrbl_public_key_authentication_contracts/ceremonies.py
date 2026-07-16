"""Canonical public-key ceremony lifecycle contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CeremonyKind(str, Enum):
    REGISTRATION = "registration"
    AUTHENTICATION = "authentication"


class CeremonyState(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    EXPIRED = "expired"
    CONSUMED = "consumed"


@dataclass(frozen=True, slots=True)
class CeremonyBinding:
    tenant_id: str
    rp_id: str
    origin: str
    principal_id: str | None = None


@dataclass(frozen=True, slots=True)
class CeremonyContext:
    ceremony_id: str
    kind: CeremonyKind
    binding: CeremonyBinding
    challenge: bytes
    issued_at: datetime
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class CeremonyReservation:
    context: CeremonyContext
    state: CeremonyState = CeremonyState.PENDING


@dataclass(frozen=True, slots=True)
class CeremonyConsumption:
    ceremony_id: str
    consumed_at: datetime
    bound_credential_id: str | None = None


__all__ = [
    "CeremonyBinding",
    "CeremonyConsumption",
    "CeremonyContext",
    "CeremonyKind",
    "CeremonyReservation",
    "CeremonyState",
]
