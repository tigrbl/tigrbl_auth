"""Policy Administration Point contracts."""

from __future__ import annotations

from importlib import import_module
from typing import Any, Mapping, Protocol


class PolicyAdministrationPointPort(Protocol):
    async def create_policy(self, payload: Mapping[str, Any], /) -> Any: ...

    async def update_policy(self, policy_id: str, payload: Mapping[str, Any], /) -> Any | None: ...

    async def publish_policy_version(self, payload: Mapping[str, Any], /) -> Any: ...

    async def create_policy_set(self, payload: Mapping[str, Any], /) -> Any: ...

    async def create_policy_target(self, payload: Mapping[str, Any], /) -> Any: ...


_SCHEMA_EXPORTS = {
    "AttributePolicyCreateRequest",
    "AttributePolicyReadResponse",
    "DelegatedAdminScopeCreateRequest",
    "DelegatedAdminScopeReadResponse",
    "PolicyConditionCreateRequest",
    "PolicyConditionReadResponse",
    "PolicyCreateRequest",
    "PolicyReadResponse",
    "PolicySetCreateRequest",
    "PolicySetMemberCreateRequest",
    "PolicyTargetCreateRequest",
    "PolicyUpdateRequest",
    "PolicyVersionCreateRequest",
    "RoleCreateRequest",
    "RoleReadResponse",
    "TenantMembershipCreateRequest",
    "TenantMembershipReadResponse",
}


def __getattr__(name: str) -> Any:
    if name not in _SCHEMA_EXPORTS:
        raise AttributeError(name)
    value = getattr(import_module("tigrbl_identity_contracts.schemas"), name)
    globals()[name] = value
    return value


__all__ = ["PolicyAdministrationPointPort"]
