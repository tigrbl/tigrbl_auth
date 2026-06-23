"""Dependency-light credential contract objects."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Mapping

from tigrbl_security_trust_contracts import ProofBinding

from .enums import CredentialKind, CredentialStatus
from .errors import CredentialStateError

UTC = timezone.utc


@dataclass(frozen=True, slots=True)
class Credential:
    id: str
    principal_id: str
    kind: CredentialKind
    secret_digest: str | None = None
    public_id: str | None = None
    status: CredentialStatus = CredentialStatus.ACTIVE
    created_at: datetime | str = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | str | None = None
    version: int = 1
    rotated_from: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        credential_id = str(self.id).strip()
        principal_id = str(self.principal_id).strip()
        if not credential_id:
            raise ValueError("credential id is required")
        if not principal_id:
            raise ValueError("principal id is required")
        object.__setattr__(self, "id", credential_id)
        object.__setattr__(self, "principal_id", principal_id)
        object.__setattr__(self, "kind", CredentialKind(self.kind))
        object.__setattr__(self, "status", CredentialStatus(self.status))
        created_at = _coerce_datetime(self.created_at, "created_at")
        object.__setattr__(self, "created_at", created_at)
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", _coerce_datetime(self.expires_at, "expires_at"))
        object.__setattr__(self, "metadata", dict(self.metadata))

    def is_expired(self, now: datetime | None = None) -> bool:
        active_now = now or datetime.now(UTC)
        if active_now.tzinfo is None:
            active_now = active_now.replace(tzinfo=UTC)
        if self.expires_at is None:
            return False
        return self.expires_at <= active_now.astimezone(UTC)

    def is_usable(self, now: datetime | None = None) -> bool:
        return self.status in {CredentialStatus.ACTIVE, CredentialStatus.PENDING} and not self.is_expired(now)

    def require_usable(self, now: datetime | None = None) -> None:
        if self.status is not CredentialStatus.ACTIVE:
            raise CredentialStateError(f"credential is not active: {self.status.value}")
        if self.is_expired(now):
            raise CredentialStateError("credential is expired")

    def with_status(self, status: CredentialStatus | str) -> "Credential":
        return replace(self, status=CredentialStatus(status))


@dataclass(frozen=True, slots=True)
class IssuedCredential:
    credential: Credential
    secret: str | None = None


def _coerce_datetime(value: datetime | str, field_name: str) -> datetime:
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"{field_name} must be an ISO datetime") from exc
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


__all__ = [
    "Credential",
    "IssuedCredential",
    "ProofBinding",
]
