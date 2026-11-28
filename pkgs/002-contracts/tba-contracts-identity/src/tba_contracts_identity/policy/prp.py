"""Policy Retrieval Point contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
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

    async def list_applicable_policies(
        self, request: PolicyRequest, /
    ) -> tuple[Any, ...]: ...

    async def resolve_policy_set(
        self, policy_set_id: str, /
    ) -> ApplicablePolicySet: ...


__all__ = [
    "ApplicablePolicySet",
    "PolicyRetrievalPointPort",
    "PolicyRetrievalRequest",
]
