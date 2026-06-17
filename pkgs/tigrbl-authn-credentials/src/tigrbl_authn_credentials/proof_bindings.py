from __future__ import annotations

"""Credential-domain proof binding models."""

from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4

from .lifecycle import Credential, CredentialKind, CredentialStatus


def _clean_tuple(values: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(value).strip() for value in values or () if str(value).strip()))


def _required_text(value: str, field_name: str) -> str:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required")
    return cleaned


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
    def for_dpop(cls, jwk_thumbprint: str, *, credential_id: str | None = None) -> "ProofBinding":
        return cls("dpop", {"jkt": jwk_thumbprint}, credential_id=credential_id)


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
    "MtlsCertificateCredential",
    "ProofBinding",
    "create_mtls_certificate_credential",
]
