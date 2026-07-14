"""Policy set contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class PolicySetReference:
    policy_set_id: str
    tenant_id: str | None = None


@dataclass(frozen=True, slots=True)
class PolicySetResolution:
    policy_set_id: str
    member_ids: tuple[str, ...] = ()
    nested_policy_set_ids: tuple[str, ...] = ()


class PolicySetRepositoryPort(Protocol):
    async def get_policy_set(self, policy_set_id: str, /) -> Any | None: ...

    async def list_members(self, policy_set_id: str, /) -> tuple[Any, ...]: ...

    async def add_member(self, payload: Mapping[str, Any], /) -> Any: ...

    async def remove_member(self, member_id: str, /) -> Any | None: ...

    async def resolve_policy_set(
        self, policy_set_id: str, /
    ) -> PolicySetResolution: ...


__all__ = [
    "PolicySetReference",
    "PolicySetRepositoryPort",
    "PolicySetResolution",
]
