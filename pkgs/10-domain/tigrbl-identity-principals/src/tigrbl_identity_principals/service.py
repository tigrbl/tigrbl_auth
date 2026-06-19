from __future__ import annotations

"""In-memory principal directory contracts used by tests and adapters."""

from dataclasses import dataclass, field

from .models import Principal, PrincipalStatus, SubjectAlias, TenantMembership


@dataclass(slots=True)
class PrincipalDirectory:
    principals: dict[str, Principal] = field(default_factory=dict)
    memberships: dict[tuple[str, str], TenantMembership] = field(default_factory=dict)
    aliases: dict[tuple[str | None, str, str], SubjectAlias] = field(default_factory=dict)

    def add_principal(self, principal: Principal) -> Principal:
        if principal.id in self.principals:
            raise ValueError(f"principal already exists: {principal.id}")
        self.principals[principal.id] = principal
        return principal

    def get_principal(self, principal_id: str) -> Principal | None:
        return self.principals.get(principal_id)

    def require_principal(self, principal_id: str) -> Principal:
        principal = self.get_principal(principal_id)
        if principal is None:
            raise KeyError(principal_id)
        return principal

    def set_status(self, principal_id: str, status: PrincipalStatus | str) -> Principal:
        principal = self.require_principal(principal_id).with_status(status)
        self.principals[principal_id] = principal
        return principal

    def add_membership(self, membership: TenantMembership) -> TenantMembership:
        if membership.principal_id not in self.principals:
            raise KeyError(membership.principal_id)
        key = (membership.tenant_id, membership.principal_id)
        self.memberships[key] = membership
        return membership

    def memberships_for_principal(self, principal_id: str) -> tuple[TenantMembership, ...]:
        return tuple(item for item in self.memberships.values() if item.principal_id == principal_id)

    def add_alias(self, alias: SubjectAlias) -> SubjectAlias:
        if alias.principal_id not in self.principals:
            raise KeyError(alias.principal_id)
        existing = self.aliases.get(alias.key)
        if existing is not None and existing.principal_id != alias.principal_id:
            raise ValueError("subject alias is already bound to another principal")
        self.aliases[alias.key] = alias
        return alias

    def resolve_alias(self, *, issuer: str, subject: str, tenant_id: str | None = None) -> Principal | None:
        alias = self.aliases.get((tenant_id, issuer, subject))
        if alias is None:
            return None
        return self.principals.get(alias.principal_id)

    def list_by_tenant(self, tenant_id: str) -> tuple[Principal, ...]:
        principal_ids = {item.principal_id for item in self.memberships.values() if item.tenant_id == tenant_id}
        return tuple(self.principals[item] for item in sorted(principal_ids) if item in self.principals)


__all__ = ["PrincipalDirectory"]
