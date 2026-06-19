from __future__ import annotations

"""Dependency-light credential lifecycle primitives."""

import hashlib
import hmac
import secrets
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4

UTC = timezone.utc


class CredentialKind(str, Enum):
    PASSWORD = "password"
    PASSWORD_RESET = "password_reset"
    PASSKEY_WEBAUTHN = "passkey_webauthn"
    API_KEY = "api_key"
    SERVICE_KEY = "service_key"
    CLIENT_SECRET = "client_secret"
    MTLS_CERTIFICATE = "mtls_certificate"
    DPOP_KEY = "dpop_key"
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



# Proof binding contracts
from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4



def _clean_tuple(values: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(value).strip() for value in values or () if str(value).strip()))


def _required_text(value: str, field_name: str) -> str:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required")
    return cleaned


def _clean_mapping(value: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)


@dataclass(frozen=True, slots=True)
class MtlsCertificateCredential:
    principal_id: str
    certificate_thumbprint: str
    id: str = field(default_factory=lambda: str(uuid4()))
    subject_dn: str | None = None
    san_dns: tuple[str, ...] = ()
    san_uri: tuple[str, ...] = ()
    san_ip: tuple[str, ...] = ()
    san_email: tuple[str, ...] = ()
    status: CredentialStatus = CredentialStatus.ACTIVE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _required_text(self.id, "credential id"))
        object.__setattr__(self, "principal_id", _required_text(self.principal_id, "principal id"))
        object.__setattr__(self, "certificate_thumbprint", _required_text(self.certificate_thumbprint, "certificate thumbprint"))
        if self.subject_dn is not None:
            object.__setattr__(self, "subject_dn", str(self.subject_dn).strip() or None)
        object.__setattr__(self, "status", CredentialStatus(self.status))
        object.__setattr__(self, "san_dns", _clean_tuple(self.san_dns))
        object.__setattr__(self, "san_uri", _clean_tuple(self.san_uri))
        object.__setattr__(self, "san_ip", _clean_tuple(self.san_ip))
        object.__setattr__(self, "san_email", _clean_tuple(self.san_email))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def confirmation_claim(self) -> dict[str, str]:
        return {"x5t#S256": self.certificate_thumbprint}

    def to_credential(self) -> Credential:
        return Credential(
            id=self.id,
            principal_id=self.principal_id,
            kind=CredentialKind.MTLS_CERTIFICATE,
            public_id=self.certificate_thumbprint,
            status=self.status,
            metadata={
                **dict(self.metadata),
                "subject_dn": self.subject_dn,
                "san_dns": list(self.san_dns),
                "san_uri": list(self.san_uri),
                "san_ip": list(self.san_ip),
                "san_email": list(self.san_email),
            },
        )


@dataclass(frozen=True, slots=True)
class DpopKeyCredential:
    principal_id: str
    jwk_thumbprint: str
    id: str = field(default_factory=lambda: str(uuid4()))
    public_jwk: Mapping[str, Any] = field(default_factory=dict)
    status: CredentialStatus = CredentialStatus.ACTIVE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _required_text(self.id, "credential id"))
        object.__setattr__(self, "principal_id", _required_text(self.principal_id, "principal id"))
        object.__setattr__(self, "jwk_thumbprint", _required_text(self.jwk_thumbprint, "JWK thumbprint"))
        object.__setattr__(self, "status", CredentialStatus(self.status))
        object.__setattr__(self, "public_jwk", _clean_mapping(self.public_jwk, "public_jwk"))
        object.__setattr__(self, "metadata", _clean_mapping(self.metadata, "metadata"))

    @property
    def confirmation_claim(self) -> dict[str, str]:
        return {"jkt": self.jwk_thumbprint}

    def to_credential(self) -> Credential:
        return Credential(
            id=self.id,
            principal_id=self.principal_id,
            kind=CredentialKind.DPOP_KEY,
            public_id=self.jwk_thumbprint,
            status=self.status,
            metadata={
                **dict(self.metadata),
                "public_jwk": dict(self.public_jwk),
            },
        )


@dataclass(frozen=True, slots=True)
class ProofBinding:
    method: str
    confirmation_claim: Mapping[str, str]
    credential_id: str | None = None

    def __post_init__(self) -> None:
        method = str(self.method).strip().lower()
        if method not in {"dpop", "mtls"}:
            raise ValueError("proof binding method must be dpop or mtls")
        claim = {
            str(key).strip(): str(value).strip()
            for key, value in self.confirmation_claim.items()
            if str(key).strip() and str(value).strip()
        }
        if method == "dpop" and not claim.get("jkt"):
            raise ValueError("DPoP proof binding requires cnf.jkt")
        if method == "mtls" and not claim.get("x5t#S256"):
            raise ValueError("mTLS proof binding requires cnf.x5t#S256")
        object.__setattr__(self, "method", method)
        object.__setattr__(self, "confirmation_claim", claim)

    @classmethod
    def for_mtls(cls, credential: MtlsCertificateCredential) -> "ProofBinding":
        return cls("mtls", credential.confirmation_claim, credential_id=credential.id)

    @classmethod
    def for_dpop(
        cls,
        jwk_thumbprint: str | DpopKeyCredential,
        *,
        credential_id: str | None = None,
    ) -> "ProofBinding":
        if isinstance(jwk_thumbprint, DpopKeyCredential):
            return cls(
                "dpop",
                jwk_thumbprint.confirmation_claim,
                credential_id=credential_id or jwk_thumbprint.id,
            )
        return cls("dpop", {"jkt": jwk_thumbprint}, credential_id=credential_id)


def create_dpop_key_credential(
    principal_id: str,
    *,
    jwk_thumbprint: str,
    public_jwk: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DpopKeyCredential:
    return DpopKeyCredential(
        principal_id=principal_id,
        jwk_thumbprint=jwk_thumbprint,
        public_jwk=dict(public_jwk or {}),
        metadata=dict(metadata or {}),
    )


def create_mtls_certificate_credential(
    principal_id: str,
    *,
    certificate_thumbprint: str,
    subject_dn: str | None = None,
    san_dns: tuple[str, ...] | list[str] | None = None,
    san_uri: tuple[str, ...] | list[str] | None = None,
    san_ip: tuple[str, ...] | list[str] | None = None,
    san_email: tuple[str, ...] | list[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> MtlsCertificateCredential:
    return MtlsCertificateCredential(
        principal_id=principal_id,
        certificate_thumbprint=certificate_thumbprint,
        subject_dn=subject_dn,
        san_dns=tuple(san_dns or ()),
        san_uri=tuple(san_uri or ()),
        san_ip=tuple(san_ip or ()),
        san_email=tuple(san_email or ()),
        metadata=dict(metadata or {}),
    )


__all__ = [
    "DpopKeyCredential",
    "MtlsCertificateCredential",
    "ProofBinding",
    "create_dpop_key_credential",
    "create_mtls_certificate_credential",
]


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
    "DpopKeyCredential",
    "IssuedCredential",
    "MtlsCertificateCredential",
    "ProofBinding",
    "consume_one_time_credential",
    "create_api_key_credential",
    "create_client_secret_credential",
    "create_dpop_key_credential",
    "create_mfa_factor_credential",
    "create_mtls_certificate_credential",
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
