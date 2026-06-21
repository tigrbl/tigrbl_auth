from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Iterable, Mapping

from ..authz.authority_roles import AuthorityRole
from .enums import NONHUMAN_PRINCIPAL_KINDS, PrincipalKind, PrincipalStatus


def _normalize_roles(values: Iterable[str | AuthorityRole] = ()) -> tuple[str, ...]:
    normalized = {str(value.value if isinstance(value, AuthorityRole) else value).strip() for value in values}
    normalized.discard("")
    return tuple(sorted(normalized))


def _normalize_attributes(values: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return dict(values or {})


@dataclass(frozen=True, slots=True)
class Realm:
    id: str
    slug: str
    name: str
    issuer: str
    status: PrincipalStatus = PrincipalStatus.ACTIVE

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("realm id is required")
        if not self.slug:
            raise ValueError("realm slug is required")
        if not self.name:
            raise ValueError("realm name is required")
        if not self.issuer:
            raise ValueError("realm issuer is required")
        object.__setattr__(self, "status", PrincipalStatus(self.status))


@dataclass(frozen=True, slots=True)
class TenantBoundary:
    tenant_id: str
    realm_id: str

    def __post_init__(self) -> None:
        if not self.tenant_id:
            raise ValueError("tenant id is required")
        if not self.realm_id:
            raise ValueError("realm id is required")


@dataclass(frozen=True, slots=True)
class Principal:
    id: str
    kind: PrincipalKind
    subject: str
    tenant_id: str | None = None
    display_name: str | None = None
    status: PrincipalStatus = PrincipalStatus.ACTIVE
    roles: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("principal id is required")
        if not self.subject:
            raise ValueError("principal subject is required")
        object.__setattr__(self, "kind", PrincipalKind(self.kind))
        object.__setattr__(self, "status", PrincipalStatus(self.status))
        object.__setattr__(self, "roles", _normalize_roles(self.roles))
        object.__setattr__(self, "attributes", _normalize_attributes(self.attributes))

    @property
    def is_human(self) -> bool:
        return self.kind in {PrincipalKind.USER, PrincipalKind.ADMIN}

    @property
    def is_nonhuman(self) -> bool:
        return self.kind in NONHUMAN_PRINCIPAL_KINDS

    @property
    def is_admin(self) -> bool:
        return AuthorityRole.ADMIN.value in self.roles or self.kind is PrincipalKind.ADMIN

    @property
    def is_owner(self) -> bool:
        return AuthorityRole.OWNER.value in self.roles

    @property
    def is_superuser(self) -> bool:
        return AuthorityRole.SUPERUSER.value in self.roles

    def with_roles(self, *roles: str | AuthorityRole) -> "Principal":
        return replace(self, roles=_normalize_roles((*self.roles, *roles)))

    def without_roles(self, *roles: str | AuthorityRole) -> "Principal":
        removed = {str(role.value if isinstance(role, AuthorityRole) else role) for role in roles}
        return replace(self, roles=tuple(role for role in self.roles if role not in removed))

    def with_status(self, status: PrincipalStatus | str) -> "Principal":
        return replace(self, status=PrincipalStatus(status))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "subject": self.subject,
            "tenant_id": self.tenant_id,
            "display_name": self.display_name,
            "status": self.status.value,
            "roles": list(self.roles),
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class TenantMembership:
    tenant_id: str
    principal_id: str
    roles: tuple[str, ...] = ()
    status: PrincipalStatus = PrincipalStatus.ACTIVE

    def __post_init__(self) -> None:
        if not self.tenant_id:
            raise ValueError("tenant id is required")
        if not self.principal_id:
            raise ValueError("principal id is required")
        object.__setattr__(self, "roles", _normalize_roles(self.roles))
        object.__setattr__(self, "status", PrincipalStatus(self.status))


@dataclass(frozen=True, slots=True)
class SubjectAlias:
    principal_id: str
    issuer: str
    subject: str
    tenant_id: str | None = None
    verified: bool = False

    def __post_init__(self) -> None:
        if not self.principal_id:
            raise ValueError("principal id is required")
        if not self.issuer:
            raise ValueError("alias issuer is required")
        if not self.subject:
            raise ValueError("alias subject is required")

    @property
    def key(self) -> tuple[str | None, str, str]:
        return (self.tenant_id, self.issuer, self.subject)


__all__ = [
    "Principal",
    "Realm",
    "SubjectAlias",
    "TenantBoundary",
    "TenantMembership",
]
