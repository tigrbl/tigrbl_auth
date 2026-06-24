"""Dependency-light identity value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import NewType
from uuid import uuid4


TenantId = NewType("TenantId", str)
RealmId = NewType("RealmId", str)
PrincipalId = NewType("PrincipalId", str)
ClientId = NewType("ClientId", str)
CredentialId = NewType("CredentialId", str)
Issuer = NewType("Issuer", str)
Subject = NewType("Subject", str)
Audience = NewType("Audience", str)
ScopeValue = NewType("ScopeValue", str)


def new_tenant_id() -> TenantId:
    return TenantId(str(uuid4()))


def new_realm_id() -> RealmId:
    return RealmId(str(uuid4()))


def new_principal_id() -> PrincipalId:
    return PrincipalId(str(uuid4()))


def new_client_id() -> ClientId:
    return ClientId(str(uuid4()))


def new_credential_id() -> CredentialId:
    return CredentialId(str(uuid4()))


@dataclass(frozen=True, slots=True)
class RealmRef:
    id: RealmId
    slug: str | None = None
    issuer: Issuer | None = None


@dataclass(frozen=True, slots=True)
class TenantRef:
    id: TenantId
    realm_id: RealmId | None = None
    slug: str | None = None


@dataclass(frozen=True, slots=True)
class PrincipalRef:
    id: PrincipalId
    tenant_id: TenantId | None = None
    subject: Subject | None = None


@dataclass(frozen=True, slots=True)
class ClientRef:
    id: ClientId
    tenant_id: TenantId | None = None
    public_client_id: str | None = None


@dataclass(frozen=True, slots=True)
class Scope:
    values: tuple[ScopeValue, ...]

    @classmethod
    def parse(cls, value: str | list[str] | tuple[str, ...] | None) -> "Scope":
        if value is None:
            return cls(())
        if isinstance(value, str):
            parts = [item for item in value.split(" ") if item]
        else:
            parts = [str(item) for item in value if str(item)]
        return cls(tuple(ScopeValue(item) for item in parts))

    def contains(self, value: str) -> bool:
        return ScopeValue(value) in self.values

    def serialize(self) -> str:
        return " ".join(str(item) for item in self.values)


__all__ = [
    "Audience",
    "ClientId",
    "ClientRef",
    "CredentialId",
    "Issuer",
    "PrincipalId",
    "PrincipalRef",
    "RealmId",
    "RealmRef",
    "Scope",
    "ScopeValue",
    "Subject",
    "TenantId",
    "TenantRef",
    "new_client_id",
    "new_credential_id",
    "new_principal_id",
    "new_realm_id",
    "new_tenant_id",
]
