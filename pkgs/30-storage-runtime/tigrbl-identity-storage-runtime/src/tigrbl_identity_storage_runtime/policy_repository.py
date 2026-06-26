"""Storage-runtime policy repository composition."""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from typing import Any

from tigrbl_identity_contracts.policy import ApplicablePolicySet, PolicyRequest
from tigrbl_identity_storage.tables import (
    Policy,
    PolicySet,
    PolicySetMember,
    PolicyTarget,
    PolicyVersion,
)


def _items(result: Any) -> tuple[Any, ...]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items") and isinstance(getattr(result, "items"), list):
        result = result.items
    if isinstance(result, tuple):
        return result
    if isinstance(result, list):
        return tuple(result)
    if result is None:
        return ()
    return (result,)


def _row_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def _path_id(value: str) -> Any:
    try:
        return uuid.UUID(str(value))
    except ValueError:
        return value


def _policy_matches_request(policy: Any, request: PolicyRequest) -> bool:
    if str(_row_value(policy, "tenant_id", "")) != str(request.tenant_id):
        return False
    status = str(_row_value(policy, "status", "active") or "active")
    if status not in {"active", "published"}:
        return False
    name = str(_row_value(policy, "name", "") or "")
    return not name or name == request.action


class StoragePolicyRepository:
    """PRP/PAP repository backed by identity storage table handlers."""

    def __init__(self, db: Any) -> None:
        self.db = db

    async def create_policy(self, payload: Mapping[str, Any], /) -> Any:
        return await Policy.handlers.create.core({"payload": dict(payload), "db": self.db})

    async def update_policy(self, policy_id: str, payload: Mapping[str, Any], /) -> Any | None:
        return await Policy.handlers.update.core(
            {
                "path_params": {"id": _path_id(policy_id)},
                "payload": dict(payload),
                "db": self.db,
            }
        )

    async def get_policy(self, policy_id: str, /) -> Any | None:
        return await Policy.handlers.read.core(
            {"path_params": {"id": _path_id(policy_id)}, "db": self.db}
        )

    async def publish_policy_version(self, payload: Mapping[str, Any], /) -> Any:
        version = await PolicyVersion.handlers.create.core(
            {"payload": dict(payload), "db": self.db}
        )
        if bool(_row_value(version, "promoted", False)):
            policy_id = str(_row_value(version, "policy_id", ""))
            if policy_id:
                await self.update_policy(
                    policy_id,
                    {
                        "active_version_id": str(_row_value(version, "id")),
                        "status": "published",
                    },
                )
        return version

    async def get_active_version(self, policy_id: str, /) -> Any | None:
        policy = await self.get_policy(policy_id)
        if policy is None:
            return None
        active_version_id = _row_value(policy, "active_version_id")
        if active_version_id:
            return await PolicyVersion.handlers.read.core(
                {
                    "path_params": {"id": _path_id(str(active_version_id))},
                    "db": self.db,
                }
            )
        versions = _items(
            await PolicyVersion.handlers.list.core(
                {
                    "payload": {"filters": {"policy_id": str(_row_value(policy, "id"))}},
                    "db": self.db,
                }
            )
        )
        promoted = [row for row in versions if bool(_row_value(row, "promoted", False))]
        if promoted:
            return sorted(
                promoted,
                key=lambda row: int(_row_value(row, "version_number", 0) or 0),
                reverse=True,
            )[0]
        return None

    async def list_applicable_policies(self, request: PolicyRequest, /) -> tuple[Any, ...]:
        rows = _items(
            await Policy.handlers.list.core(
                {
                    "payload": {"filters": {"tenant_id": request.tenant_id}},
                    "db": self.db,
                }
            )
        )
        return tuple(row for row in rows if _policy_matches_request(row, request))

    async def create_policy_set(self, payload: Mapping[str, Any], /) -> Any:
        return await PolicySet.handlers.create.core({"payload": dict(payload), "db": self.db})

    async def get_policy_set(self, policy_set_id: str, /) -> Any | None:
        return await PolicySet.handlers.read.core(
            {"path_params": {"id": _path_id(policy_set_id)}, "db": self.db}
        )

    async def add_member(self, payload: Mapping[str, Any], /) -> Any:
        return await PolicySetMember.handlers.create.core(
            {"payload": dict(payload), "db": self.db}
        )

    async def list_members(self, policy_set_id: str, /) -> tuple[Any, ...]:
        rows = _items(
            await PolicySetMember.handlers.list.core(
                {
                    "payload": {"filters": {"policy_set_id": policy_set_id}},
                    "db": self.db,
                }
            )
        )
        return tuple(
            sorted(
                rows,
                key=lambda row: int(_row_value(row, "priority", 0) or 0),
            )
        )

    async def remove_member(self, member_id: str, /) -> Any | None:
        member = await PolicySetMember.handlers.read.core(
            {"path_params": {"id": _path_id(member_id)}, "db": self.db}
        )
        if member is None:
            return None
        await PolicySetMember.handlers.delete.core(
            {"path_params": {"id": _path_id(member_id)}, "db": self.db}
        )
        return member

    async def resolve_policy_set(self, policy_set_id: str, /) -> ApplicablePolicySet:
        members = await self.list_members(policy_set_id)
        return ApplicablePolicySet(
            policy_set_id=policy_set_id,
            policy_ids=tuple(
                str(_row_value(row, "member_id"))
                for row in members
                if _row_value(row, "member_kind") == "policy"
            ),
            target_ids=tuple(
                str(_row_value(row, "member_id"))
                for row in members
                if _row_value(row, "member_kind") == "target"
            ),
        )

    async def create_policy_target(self, payload: Mapping[str, Any], /) -> Any:
        return await PolicyTarget.handlers.create.core(
            {"payload": dict(payload), "db": self.db}
        )


def create_storage_policy_repository(db: Any) -> StoragePolicyRepository:
    return StoragePolicyRepository(db)


__all__ = ["StoragePolicyRepository", "create_storage_policy_repository"]
