"""Dependency-light credential contract objects."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

from .enums import CredentialAuditAction, CredentialKind, CredentialStatus
from .errors import CredentialStateError

UTC = timezone.utc


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
            expires_at = (
                self.expires_at.replace(tzinfo=UTC)
                if self.expires_at.tzinfo is None
                else self.expires_at.astimezone(UTC)
            )
            object.__setattr__(self, "expires_at", expires_at)
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
        object.__setattr__(
            self,
            "certificate_thumbprint",
            _required_text(self.certificate_thumbprint, "certificate thumbprint"),
        )
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
            metadata={**dict(self.metadata), "public_jwk": dict(self.public_jwk)},
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


__all__ = [
    "Credential",
    "CredentialAuditEvent",
    "DpopKeyCredential",
    "IssuedCredential",
    "MtlsCertificateCredential",
    "ProofBinding",
]
