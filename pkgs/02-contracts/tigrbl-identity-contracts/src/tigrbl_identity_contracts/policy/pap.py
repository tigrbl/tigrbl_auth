"""Policy Administration Point contracts."""

from __future__ import annotations

from typing import Any, Mapping, Protocol


class PolicyAdministrationPointPort(Protocol):
    async def create_policy(self, payload: Mapping[str, Any], /) -> Any: ...

    async def update_policy(
        self, policy_id: str, payload: Mapping[str, Any], /
    ) -> Any | None: ...

    async def publish_policy_version(self, payload: Mapping[str, Any], /) -> Any: ...

    async def create_policy_set(self, payload: Mapping[str, Any], /) -> Any: ...

    async def create_policy_target(self, payload: Mapping[str, Any], /) -> Any: ...


__all__ = ["PolicyAdministrationPointPort"]
