"""Canonical digital credential artifact contracts."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping

from .formats import CredentialFormat


@dataclass(frozen=True, slots=True)
class DigitalCredential:
    format: CredentialFormat
    payload: bytes | str
    issuer: str | None = None
    subject: str | None = None
    issued_at: datetime | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


__all__ = ["DigitalCredential"]
