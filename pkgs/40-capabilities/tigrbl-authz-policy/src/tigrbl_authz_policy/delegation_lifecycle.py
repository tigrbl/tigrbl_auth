"""Delegation-grant lifecycle public compatibility surface."""

from __future__ import annotations

from typing import Iterable

from tigrbl_identity_contracts.authority import AuthorityScope
from tigrbl_identity_contracts.delegation import (
    ACTIVE_GRANT_STATUSES,
    DELEGATION_GRANT_UIX_WORKFLOWS,
    MANAGEMENT_DELEGATION_SURFACES,
    TERMINAL_GRANT_STATUSES,
    DelegationGrantEvaluation,
    DelegationGrantLifecycleEntry,
    DelegationLifecycleAuditEvent,
    DelegationTokenLink,
)

from ._delegation_lifecycle_service import (
    DelegationGrantLifecycleService,
    assert_delegation_management_surface,
    delegation_grant_uix_workflows,
)


def _normalize_values(values: Iterable[str] | None, *, default: tuple[str, ...] = ()) -> tuple[str, ...]:
    normalized = {str(value).strip() for value in values or default if str(value).strip()}
    return tuple(sorted(normalized))


def normalize_delegation_scopes(
    *,
    tenant_ids: Iterable[str],
    actions: Iterable[str],
    resources: Iterable[str] | None = None,
    realm: str = "",
) -> tuple[AuthorityScope, ...]:
    tenants = _normalize_values(tenant_ids)
    normalized_actions = _normalize_values(actions)
    normalized_resources = _normalize_values(resources, default=("*",))
    if not tenants:
        raise ValueError("at least one tenant_id is required")
    if not normalized_actions:
        raise ValueError("at least one action is required")
    return tuple(
        AuthorityScope(tenant_id=tenant, realm=realm, action=action, resource=resource)
        for tenant in tenants
        for action in normalized_actions
        for resource in normalized_resources
    )


__all__ = [
    "ACTIVE_GRANT_STATUSES",
    "DELEGATION_GRANT_UIX_WORKFLOWS",
    "MANAGEMENT_DELEGATION_SURFACES",
    "TERMINAL_GRANT_STATUSES",
    "DelegationGrantEvaluation",
    "DelegationGrantLifecycleEntry",
    "DelegationGrantLifecycleService",
    "DelegationLifecycleAuditEvent",
    "DelegationTokenLink",
    "assert_delegation_management_surface",
    "delegation_grant_uix_workflows",
    "normalize_delegation_scopes",
]
