from __future__ import annotations

from typing import Any, Iterable, Mapping

from tigrbl_identity_core.normalization import row_value as _row_value
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.policy.conditions import DynamicCondition
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_authorization_policy_durability import (
    AttributePolicyTable as _StoredAttributePolicy,
)
from tigrbl_authz_policy_rules_concrete import AttributePolicy


def _condition_contract(row: Any) -> DynamicCondition:
    return DynamicCondition(
        field=str(_row_value(row, "field_name") or ""),
        operator=str(_row_value(row, "operator") or ""),
        expected=_row_value(row, "expected"),
    )


def _attribute_policy_contract(
    row: Any, conditions: Iterable[Any] = ()
) -> AttributePolicy:
    return AttributePolicy(
        name=str(_row_value(row, "name") or ""),
        permission=str(_row_value(row, "permission") or ""),
        tenant_id=_row_value(row, "tenant_id"),
        client_id=_row_value(row, "client_id"),
        effect=str(_row_value(row, "effect", "allow") or "allow"),
        required_attributes=dict(_row_value(row, "required_attributes", {}) or {}),
        dynamic_conditions=tuple(
            _condition_contract(condition) for condition in conditions
        ),
    )


class ABACAdministrator:
    def __init__(self, db: Any) -> None:
        self.db = db

    async def upsert_policy(
        self,
        name: str,
        *,
        permission: str,
        required_attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        dynamic_conditions: Iterable[DynamicCondition] = (),
        effect: str = "allow",
        client_id: str | None = None,
    ) -> AttributePolicy:
        if not name or not permission or not required_attributes:
            raise ValueError("policy name, permission, and attributes are required")
        (
            row,
            conditions,
        ) = await _StoredAttributePolicy.handlers.upsert_with_conditions.core(
            {
                "payload": {
                    "name": name,
                    "tenant_id": tenant_id,
                    "client_id": client_id,
                    "permission": permission,
                    "effect": effect,
                    "required_attributes": dict(required_attributes),
                    "dynamic_conditions": tuple(
                        {
                            "field_name": condition.field,
                            "operator": condition.operator,
                            "expected": condition.expected,
                        }
                        for condition in dynamic_conditions
                    ),
                },
                "db": self.db,
            }
        )
        return _attribute_policy_contract(row, conditions)

    async def has_relevant_policy(
        self,
        permission: str,
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> bool:
        return bool(
            await self._matching_policies(
                permission, tenant_id=tenant_id, client_id=client_id
            )
        )

    async def decide(
        self,
        *,
        permission: str,
        attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> PolicyDecision:
        allow_matches: list[str] = []
        deny_matches: list[str] = []
        for policy in await self._matching_policies(
            permission, tenant_id=tenant_id, client_id=client_id
        ):
            if not all(
                attributes.get(key) == value
                for key, value in policy.required_attributes.items()
            ):
                continue
            if not all(
                condition.evaluate(attributes)
                for condition in policy.dynamic_conditions
            ):
                continue
            if policy.effect == "deny":
                deny_matches.append(policy.name)
            else:
                allow_matches.append(policy.name)
        if deny_matches:
            return PolicyDecision(
                False,
                "permission denied by ABAC attributes",
                tuple(sorted(deny_matches)),
            )
        if allow_matches:
            return PolicyDecision(
                True,
                "permission granted by matching attributes",
                tuple(sorted(allow_matches)),
            )
        return PolicyDecision(False, "permission denied by ABAC attributes", ())

    async def list_policies(self) -> tuple[AttributePolicy, ...]:
        return tuple(
            _attribute_policy_contract(row, conditions)
            for row, conditions in await _StoredAttributePolicy.handlers.list_active_with_conditions.core(
                {"payload": {"tenant_id": None}, "db": self.db}
            )
        )

    async def summary(self) -> dict[str, Any]:
        policies = await self.list_policies()
        return {
            "policy_count": len(policies),
            "policies": [policy.name for policy in policies],
        }

    async def _matching_policies(
        self,
        permission: str,
        *,
        tenant_id: str | None,
        client_id: str | None,
    ) -> tuple[AttributePolicy, ...]:
        policies = await self.list_policies()
        return tuple(
            policy
            for policy in policies
            if _permission_matches(policy.permission, permission)
            and policy.tenant_id in {None, tenant_id}
            and policy.client_id in {None, client_id}
        )


__all__ = [
    "ABACAdministrator",
    "AttributePolicy",
    "DynamicCondition",
]
