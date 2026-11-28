"""Results shared by record-backed authentication capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field

from .authenticators import AuthenticationEvidence


@dataclass(frozen=True, slots=True)
class RecordAuthenticationResult:
    authenticated: bool
    record: object | None = None
    credential_record: object | None = None
    principal_kind: str | None = None
    evidence: AuthenticationEvidence = field(default_factory=AuthenticationEvidence)
    reason: str | None = None


__all__ = ["RecordAuthenticationResult"]
