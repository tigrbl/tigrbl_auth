from __future__ import annotations

"""First-class principal model objects for identity package consumers."""

from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_contracts.authority import AuthorityRole
from tigrbl_identity_contracts.principals import (
    NONHUMAN_PRINCIPAL_KINDS,
    Principal,
    PrincipalKind,
    PrincipalStatus,
    Realm,
    SubjectAlias,
    TenantBoundary,
    TenantMembership,
)


def new_principal_id() -> str:
    return str(uuid4())


def _normalize_roles(values: Iterable[str | AuthorityRole] = ()) -> tuple[str, ...]:
    normalized = {str(value.value if isinstance(value, AuthorityRole) else value).strip() for value in values}
    normalized.discard("")
    return tuple(sorted(normalized))


def _normalize_attributes(values: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return dict(values or {})


def create_user_principal(
    subject: str,
    *,
    id: str | None = None,
    tenant_id: str | None = None,
    display_name: str | None = None,
    roles: Iterable[str | AuthorityRole] = (),
    attributes: Mapping[str, Any] | None = None,
) -> Principal:
    return Principal(
        id=id or new_principal_id(),
        kind=PrincipalKind.USER,
        subject=subject,
        tenant_id=tenant_id,
        display_name=display_name,
        roles=_normalize_roles(roles),
        attributes=_normalize_attributes(attributes),
    )


def create_admin_principal(
    subject: str,
    *,
    id: str | None = None,
    tenant_id: str | None = None,
    owner: bool = False,
    superuser: bool = False,
    roles: Iterable[str | AuthorityRole] = (),
) -> Principal:
    role_values: list[str | AuthorityRole] = [AuthorityRole.ADMIN, *roles]
    if owner:
        role_values.append(AuthorityRole.OWNER)
    if superuser:
        role_values.append(AuthorityRole.SUPERUSER)
    return Principal(
        id=id or new_principal_id(),
        kind=PrincipalKind.ADMIN,
        subject=subject,
        tenant_id=tenant_id,
        roles=_normalize_roles(role_values),
    )


def create_nonhuman_principal(
    kind: PrincipalKind | str,
    subject: str,
    *,
    id: str | None = None,
    tenant_id: str | None = None,
    display_name: str | None = None,
    attributes: Mapping[str, Any] | None = None,
) -> Principal:
    principal_kind = PrincipalKind(kind)
    if principal_kind not in NONHUMAN_PRINCIPAL_KINDS:
        raise ValueError(f"{principal_kind.value!r} is not a nonhuman principal kind")
    return Principal(
        id=id or new_principal_id(),
        kind=principal_kind,
        subject=subject,
        tenant_id=tenant_id,
        display_name=display_name,
        attributes=_normalize_attributes(attributes),
    )


def create_service_principal(subject: str, **kwargs: Any) -> Principal:
    return create_nonhuman_principal(PrincipalKind.SERVICE, subject, **kwargs)


def create_app_principal(subject: str, **kwargs: Any) -> Principal:
    return create_nonhuman_principal(PrincipalKind.APP, subject, **kwargs)


def create_machine_principal(subject: str, **kwargs: Any) -> Principal:
    return create_nonhuman_principal(PrincipalKind.MACHINE, subject, **kwargs)


def create_workload_principal(subject: str, **kwargs: Any) -> Principal:
    return create_nonhuman_principal(PrincipalKind.WORKLOAD, subject, **kwargs)


def create_device_principal(subject: str, **kwargs: Any) -> Principal:
    return create_nonhuman_principal(PrincipalKind.DEVICE, subject, **kwargs)


def membership_for(principal: Principal, tenant_id: str, roles: Iterable[str | AuthorityRole] = ()) -> TenantMembership:
    return TenantMembership(tenant_id=tenant_id, principal_id=principal.id, roles=_normalize_roles(roles))


def alias_for(
    principal: Principal,
    *,
    issuer: str,
    subject: str,
    tenant_id: str | None = None,
    verified: bool = False,
) -> SubjectAlias:
    return SubjectAlias(
        principal_id=principal.id,
        issuer=issuer,
        subject=subject,
        tenant_id=tenant_id if tenant_id is not None else principal.tenant_id,
        verified=verified,
    )


__all__ = [
    "AuthorityRole",
    "NONHUMAN_PRINCIPAL_KINDS",
    "Principal",
    "PrincipalKind",
    "PrincipalStatus",
    "Realm",
    "SubjectAlias",
    "TenantBoundary",
    "TenantMembership",
    "alias_for",
    "create_admin_principal",
    "create_app_principal",
    "create_device_principal",
    "create_machine_principal",
    "create_nonhuman_principal",
    "create_service_principal",
    "create_user_principal",
    "create_workload_principal",
    "membership_for",
    "new_principal_id",
]
