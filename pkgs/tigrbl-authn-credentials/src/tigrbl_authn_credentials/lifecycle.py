from __future__ import annotations

"""Dependency-light credential lifecycle primitives."""

import hashlib
import hmac
import secrets
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4


class CredentialKind(str, Enum):
    PASSWORD = "password"
    PASSWORD_RESET = "password_reset"
    PASSKEY_WEBAUTHN = "passkey_webauthn"
    API_KEY = "api_key"
    SERVICE_KEY = "service_key"
    CLIENT_SECRET = "client_secret"
    MFA_FACTOR = "mfa_factor"


class CredentialStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ROTATED = "rotated"
    REVOKED = "revoked"
    EXPIRED = "expired"
    CONSUMED = "consumed"


class CredentialAuditAction(str, Enum):
    CREATED = "created"
    VERIFIED = "verified"
    FAILED = "failed"
    ROTATED = "rotated"
    REVOKED = "revoked"
    CONSUMED = "consumed"


class CredentialError(Exception):
    """Base credential lifecycle error."""


class CredentialVerificationError(CredentialError):
    """Raised when presented credential material does not verify."""


class CredentialStateError(CredentialError):
    """Raised when a credential is not usable in its current lifecycle state."""


@dataclass(frozen=True, slots=True)
class CredentialAuditEvent:
    id: str
    credential_id: str
    action: CredentialAuditAction
    occurred_at: datetime
    principal_id: str | None = None
    actor: str | None = None
    outcome: str = "ok"
    reason: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "action", CredentialAuditAction(self.action))
        if self.occurred_at.tzinfo is None:
            object.__setattr__(self, "occurred_at", self.occurred_at.replace(tzinfo=UTC))
        else:
            object.__setattr__(self, "occurred_at", self.occurred_at.astimezone(UTC))


@dataclass(frozen=True, slots=True)
class Credential:
    id: str
    principal_id: str
    kind: CredentialKind
    secret_digest: str | None = None
    public_id: str | None = None
    status: CredentialStatus = CredentialStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None
    version: int = 1
    rotated_from: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("credential id is required")
        if not self.principal_id:
            raise ValueError("principal id is required")
        object.__setattr__(self, "kind", CredentialKind(self.kind))
        object.__setattr__(self, "status", CredentialStatus(self.status))
        if self.created_at.tzinfo is None:
            object.__setattr__(self, "created_at", self.created_at.replace(tzinfo=UTC))
        else:
            object.__setattr__(self, "created_at", self.created_at.astimezone(UTC))
        if self.expires_at is not None:
            object.__setattr__(
                self,
                "expires_at",
                self.expires_at.replace(tzinfo=UTC) if self.expires_at.tzinfo is None else self.expires_at.astimezone(UTC),
            )
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


def new_credential_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(UTC)


def hash_secret(secret: str, *, salt: str | None = None, iterations: int = 120_000) -> str:
    if not secret:
        raise ValueError("secret is required")
    active_salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), active_salt.encode("utf-8"), iterations).hex()
    return f"pbkdf2_sha256${iterations}${active_salt}${digest}"


def verify_secret(secret: str, encoded: str | None) -> bool:
    if not encoded:
        return False
    try:
        algorithm, iterations_raw, salt, expected = encoded.split("$", 3)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    actual = hash_secret(secret, salt=salt, iterations=int(iterations_raw)).split("$", 3)[3]
    return hmac.compare_digest(actual, expected)


def issue_shared_secret(
    principal_id: str,
    kind: CredentialKind | str,
    *,
    secret: str | None = None,
    public_id: str | None = None,
    ttl: timedelta | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> IssuedCredential:
    active_secret = secret or secrets.token_urlsafe(32)
    now = utc_now()
    credential = Credential(
        id=new_credential_id(),
        principal_id=principal_id,
        kind=CredentialKind(kind),
        secret_digest=hash_secret(active_secret),
        public_id=public_id,
        created_at=now,
        expires_at=now + ttl if ttl is not None else None,
        metadata=dict(metadata or {}),
    )
    return IssuedCredential(credential=credential, secret=active_secret)


def create_password_credential(principal_id: str, password: str) -> Credential:
    return issue_shared_secret(principal_id, CredentialKind.PASSWORD, secret=password).credential


def create_password_reset_credential(principal_id: str, *, ttl: timedelta = timedelta(minutes=15)) -> IssuedCredential:
    return issue_shared_secret(principal_id, CredentialKind.PASSWORD_RESET, ttl=ttl, metadata={"one_time": True})


def create_api_key_credential(principal_id: str, *, public_id: str | None = None) -> IssuedCredential:
    return issue_shared_secret(principal_id, CredentialKind.API_KEY, public_id=public_id or f"ak_{secrets.token_hex(8)}")


def create_service_key_credential(principal_id: str, *, public_id: str | None = None) -> IssuedCredential:
    return issue_shared_secret(principal_id, CredentialKind.SERVICE_KEY, public_id=public_id or f"sk_{secrets.token_hex(8)}")


def create_client_secret_credential(principal_id: str, *, public_id: str | None = None) -> IssuedCredential:
    return issue_shared_secret(principal_id, CredentialKind.CLIENT_SECRET, public_id=public_id or f"cs_{secrets.token_hex(8)}")


def create_mfa_factor_credential(principal_id: str, factor_secret: str, *, factor_type: str = "totp") -> Credential:
    return issue_shared_secret(
        principal_id,
        CredentialKind.MFA_FACTOR,
        secret=factor_secret,
        metadata={"factor_type": factor_type},
    ).credential


def create_passkey_credential(
    principal_id: str,
    *,
    credential_id: str,
    public_key: str,
    sign_count: int = 0,
) -> Credential:
    if not credential_id:
        raise ValueError("passkey credential_id is required")
    if not public_key:
        raise ValueError("passkey public_key is required")
    return Credential(
        id=new_credential_id(),
        principal_id=principal_id,
        kind=CredentialKind.PASSKEY_WEBAUTHN,
        public_id=credential_id,
        metadata={"credential_id": credential_id, "public_key": public_key, "sign_count": int(sign_count)},
    )


def verify_credential(credential: Credential, presented_secret: str, *, now: datetime | None = None) -> bool:
    credential.require_usable(now)
    if credential.kind is CredentialKind.PASSKEY_WEBAUTHN:
        return hmac.compare_digest(str(credential.public_id or ""), presented_secret)
    return verify_secret(presented_secret, credential.secret_digest)


def rotate_credential(credential: Credential, *, new_secret: str | None = None) -> IssuedCredential:
    if credential.status is CredentialStatus.REVOKED:
        raise CredentialStateError("revoked credential cannot be rotated")
    issued = issue_shared_secret(
        credential.principal_id,
        credential.kind,
        secret=new_secret,
        public_id=credential.public_id,
        metadata=credential.metadata,
    )
    return IssuedCredential(
        credential=replace(issued.credential, version=credential.version + 1, rotated_from=credential.id),
        secret=issued.secret,
    )


def revoke_credential(credential: Credential, *, reason: str | None = None) -> Credential:
    metadata = dict(credential.metadata)
    if reason:
        metadata["revocation_reason"] = reason
    return replace(credential, status=CredentialStatus.REVOKED, metadata=metadata)


def consume_one_time_credential(credential: Credential, presented_secret: str) -> Credential:
    if credential.metadata.get("one_time") is not True:
        raise CredentialStateError("credential is not one-time")
    if not verify_credential(credential, presented_secret):
        raise CredentialVerificationError("credential verification failed")
    return replace(credential, status=CredentialStatus.CONSUMED)


@dataclass(slots=True)
class CredentialLedger:
    credentials: dict[str, Credential] = field(default_factory=dict)
    audit_events: list[CredentialAuditEvent] = field(default_factory=list)

    def record(self, credential: Credential, action: CredentialAuditAction | str, *, outcome: str = "ok", reason: str | None = None, actor: str | None = None) -> CredentialAuditEvent:
        event = CredentialAuditEvent(
            id=str(uuid4()),
            credential_id=credential.id,
            principal_id=credential.principal_id,
            action=CredentialAuditAction(action),
            occurred_at=utc_now(),
            actor=actor,
            outcome=outcome,
            reason=reason,
        )
        self.audit_events.append(event)
        return event

    def add(self, credential: Credential) -> Credential:
        if credential.id in self.credentials:
            raise ValueError(f"credential already exists: {credential.id}")
        self.credentials[credential.id] = credential
        self.record(credential, CredentialAuditAction.CREATED)
        return credential

    def verify(self, credential_id: str, presented_secret: str) -> bool:
        credential = self.credentials[credential_id]
        try:
            ok = verify_credential(credential, presented_secret)
        except CredentialError as exc:
            self.record(credential, CredentialAuditAction.FAILED, outcome="denied", reason=str(exc))
            raise
        self.record(credential, CredentialAuditAction.VERIFIED if ok else CredentialAuditAction.FAILED, outcome="ok" if ok else "denied")
        return ok

    def rotate(self, credential_id: str, *, new_secret: str | None = None) -> IssuedCredential:
        current = self.credentials[credential_id]
        issued = rotate_credential(current, new_secret=new_secret)
        self.credentials[current.id] = current.with_status(CredentialStatus.ROTATED)
        self.credentials[issued.credential.id] = issued.credential
        self.record(current, CredentialAuditAction.ROTATED)
        self.record(issued.credential, CredentialAuditAction.CREATED)
        return issued

    def revoke(self, credential_id: str, *, reason: str | None = None) -> Credential:
        revoked = revoke_credential(self.credentials[credential_id], reason=reason)
        self.credentials[credential_id] = revoked
        self.record(revoked, CredentialAuditAction.REVOKED, reason=reason)
        return revoked


__all__ = [
    "Credential",
    "CredentialAuditAction",
    "CredentialAuditEvent",
    "CredentialError",
    "CredentialKind",
    "CredentialLedger",
    "CredentialStateError",
    "CredentialStatus",
    "CredentialVerificationError",
    "IssuedCredential",
    "consume_one_time_credential",
    "create_api_key_credential",
    "create_client_secret_credential",
    "create_mfa_factor_credential",
    "create_passkey_credential",
    "create_password_credential",
    "create_password_reset_credential",
    "create_service_key_credential",
    "hash_secret",
    "issue_shared_secret",
    "new_credential_id",
    "revoke_credential",
    "rotate_credential",
    "utc_now",
    "verify_credential",
    "verify_secret",
]
