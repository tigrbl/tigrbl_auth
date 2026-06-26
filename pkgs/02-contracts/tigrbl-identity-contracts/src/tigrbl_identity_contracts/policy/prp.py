"""Policy Retrieval Point contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, Mapping, Protocol

from .requests import PolicyRequest


@dataclass(frozen=True, slots=True)
class PolicyRetrievalRequest:
    tenant_id: str
    subject: str
    action: str
    resource: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ApplicablePolicySet:
    policy_set_id: str
    policy_ids: tuple[str, ...] = ()
    target_ids: tuple[str, ...] = ()


class PolicyRetrievalPointPort(Protocol):
    async def get_policy(self, policy_id: str, /) -> Any | None: ...

    async def get_active_version(self, policy_id: str, /) -> Any | None: ...

    async def list_applicable_policies(self, request: PolicyRequest, /) -> tuple[Any, ...]: ...

    async def resolve_policy_set(self, policy_set_id: str, /) -> ApplicablePolicySet: ...


_SCHEMA_EXPORTS = {
    "PolicyCreateRequest",
    "PolicyReadResponse",
    "PolicyUpdateRequest",
    "PolicyVersionCreateRequest",
    "PolicyVersionReadResponse",
    "PolicyVersionUpdateRequest",
    "PolicySetCreateRequest",
    "PolicySetReadResponse",
    "PolicySetUpdateRequest",
    "PolicySetMemberCreateRequest",
    "PolicySetMemberReadResponse",
    "PolicySetMemberUpdateRequest",
    "PolicyTargetCreateRequest",
    "PolicyTargetReadResponse",
    "PolicyTargetUpdateRequest",
}


def __getattr__(name: str) -> Any:
    if name not in _SCHEMA_EXPORTS:
        raise AttributeError(name)
    value = getattr(import_module("tigrbl_identity_contracts.schemas"), name)
    globals()[name] = value
    return value


__all__ = [
    "ApplicablePolicySet",
    "PolicyRetrievalPointPort",
    "PolicyRetrievalRequest",
]
