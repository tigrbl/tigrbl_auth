from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4

from tigrbl_identity_contracts.credentials import (
    Credential,
    CredentialKind,
    CredentialStatus,
)
from tigrbl_identity_model_bases import CredentialBase


def _new_credential_id() -> str:
    return str(uuid4())


def _required_text(value: str, field_name: str) -> str:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required")
    return cleaned


def _clean_tuple(values: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(value).strip() for value in values or () if str(value).strip()))


def _clean_mapping(value: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)


@dataclass(frozen=True, slots=True, kw_only=True)
class PasswordCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.PASSWORD, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class PasswordResetCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.PASSWORD_RESET, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiKeyCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.API_KEY, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceKeyCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.SERVICE_KEY, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class ClientSecretCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.CLIENT_SECRET, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class MfaCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.MFA_FACTOR, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class PasskeyCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.PASSKEY_WEBAUTHN, init=False)
    credential_id: str
    public_key: str
    sign_count: int = 0

    def __post_init__(self) -> None:
        credential_id = _required_text(self.credential_id, "credential id")
        public_key = _required_text(self.public_key, "public key")
        object.__setattr__(self, "credential_id", credential_id)
        object.__setattr__(self, "public_key", public_key)
        object.__setattr__(self, "public_id", self.public_id or credential_id)
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "credential_id": credential_id,
                "public_key": public_key,
                "sign_count": int(self.sign_count),
            },
        )
        CredentialBase.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceCredential(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.SERVICE_KEY, init=False)
    credential_id: str
    service_id: str
    label: str
    raw_key: str
    revoked: bool = False

    def __post_init__(self) -> None:
        credential_id = _required_text(self.credential_id, "credential id")
        service_id = _required_text(self.service_id, "service id")
        object.__setattr__(self, "credential_id", credential_id)
        object.__setattr__(self, "service_id", service_id)
        object.__setattr__(self, "id", self.id or credential_id)
        object.__setattr__(self, "principal_id", self.principal_id or service_id)
        object.__setattr__(self, "public_id", self.public_id or credential_id)
        object.__setattr__(
            self,
            "secret_digest",
            self.secret_digest or f"raw:{_required_text(self.raw_key, 'raw key')}",
        )
        object.__setattr__(
            self,
            "status",
            CredentialStatus.REVOKED if self.revoked else self.status,
        )
        CredentialBase.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class WebAuthnCredential(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.PASSKEY_WEBAUTHN, init=False)
    credential_id: str
    subject_id: str
    tenant_id: str
    rp_id: str
    algorithm: str
    transports: tuple[str, ...]
    sign_count: int = 0
    revoked: bool = False

    def __post_init__(self) -> None:
        credential_id = _required_text(self.credential_id, "credential id")
        subject_id = _required_text(self.subject_id, "subject id")
        object.__setattr__(self, "credential_id", credential_id)
        object.__setattr__(self, "subject_id", subject_id)
        object.__setattr__(self, "id", self.id or credential_id)
        object.__setattr__(self, "principal_id", self.principal_id or subject_id)
        object.__setattr__(self, "public_id", self.public_id or credential_id)
        object.__setattr__(self, "transports", _clean_tuple(self.transports))
        object.__setattr__(
            self,
            "status",
            CredentialStatus.REVOKED if self.revoked else self.status,
        )
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "tenant_id": self.tenant_id,
                "rp_id": self.rp_id,
                "algorithm": self.algorithm,
                "transports": list(self.transports),
                "sign_count": int(self.sign_count),
            },
        )
        CredentialBase.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class PasswordlessCredential(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.PASSWORD_RESET, init=False)
    credential_id: str
    subject_id: str
    tenant_id: str
    credential_kind: str
    recovery_codes: tuple[str, ...]
    revoked: bool = False

    def __post_init__(self) -> None:
        credential_id = _required_text(self.credential_id, "credential id")
        subject_id = _required_text(self.subject_id, "subject id")
        object.__setattr__(self, "credential_id", credential_id)
        object.__setattr__(self, "subject_id", subject_id)
        object.__setattr__(self, "id", self.id or credential_id)
        object.__setattr__(self, "principal_id", self.principal_id or subject_id)
        object.__setattr__(self, "public_id", self.public_id or credential_id)
        object.__setattr__(self, "recovery_codes", _clean_tuple(self.recovery_codes))
        object.__setattr__(
            self,
            "status",
            CredentialStatus.REVOKED if self.revoked else self.status,
        )
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "tenant_id": self.tenant_id,
                "credential_kind": self.credential_kind,
                "recovery_codes": list(self.recovery_codes),
            },
        )
        CredentialBase.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class MfaFactor(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.MFA_FACTOR, init=False)
    factor_id: str
    subject_id: str
    tenant_id: str
    method: str
    bound_credential_id: str | None = None
    revoked: bool = False

    def __post_init__(self) -> None:
        factor_id = _required_text(self.factor_id, "factor id")
        subject_id = _required_text(self.subject_id, "subject id")
        object.__setattr__(self, "factor_id", factor_id)
        object.__setattr__(self, "subject_id", subject_id)
        object.__setattr__(self, "id", self.id or factor_id)
        object.__setattr__(self, "principal_id", self.principal_id or subject_id)
        object.__setattr__(self, "public_id", self.public_id or factor_id)
        object.__setattr__(
            self,
            "status",
            CredentialStatus.REVOKED if self.revoked else self.status,
        )
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "tenant_id": self.tenant_id,
                "method": self.method,
                "bound_credential_id": self.bound_credential_id,
            },
        )
        CredentialBase.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class MtlsCertificateCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.MTLS_CERTIFICATE, init=False)
    certificate_thumbprint: str
    subject_dn: str | None = None
    san_dns: tuple[str, ...] = ()
    san_uri: tuple[str, ...] = ()
    san_ip: tuple[str, ...] = ()
    san_email: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        certificate_thumbprint = _required_text(self.certificate_thumbprint, "certificate thumbprint")
        object.__setattr__(self, "certificate_thumbprint", certificate_thumbprint)
        if self.subject_dn is not None:
            object.__setattr__(self, "subject_dn", str(self.subject_dn).strip() or None)
        object.__setattr__(self, "public_id", self.public_id or certificate_thumbprint)
        object.__setattr__(self, "san_dns", _clean_tuple(self.san_dns))
        object.__setattr__(self, "san_uri", _clean_tuple(self.san_uri))
        object.__setattr__(self, "san_ip", _clean_tuple(self.san_ip))
        object.__setattr__(self, "san_email", _clean_tuple(self.san_email))
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "subject_dn": self.subject_dn,
                "san_dns": list(self.san_dns),
                "san_uri": list(self.san_uri),
                "san_ip": list(self.san_ip),
                "san_email": list(self.san_email),
            },
        )
        CredentialBase.__post_init__(self)

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
            metadata=self.metadata,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DpopKeyCredential(CredentialBase):
    id: str = field(default_factory=_new_credential_id)
    kind: CredentialKind = field(default=CredentialKind.DPOP_KEY, init=False)
    jwk_thumbprint: str
    public_jwk: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        jwk_thumbprint = _required_text(self.jwk_thumbprint, "JWK thumbprint")
        object.__setattr__(self, "jwk_thumbprint", jwk_thumbprint)
        object.__setattr__(self, "public_id", self.public_id or jwk_thumbprint)
        object.__setattr__(self, "public_jwk", _clean_mapping(self.public_jwk, "public_jwk"))
        object.__setattr__(
            self,
            "metadata",
            {**dict(self.metadata), "public_jwk": dict(self.public_jwk)},
        )
        CredentialBase.__post_init__(self)

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
            metadata=self.metadata,
        )


__all__ = [
    "ApiKeyCredential",
    "ClientSecretCredential",
    "DpopKeyCredential",
    "MfaCredential",
    "MfaFactor",
    "MtlsCertificateCredential",
    "PasskeyCredential",
    "PasswordCredential",
    "PasswordResetCredential",
    "PasswordlessCredential",
    "ServiceCredential",
    "ServiceKeyCredential",
    "WebAuthnCredential",
]
