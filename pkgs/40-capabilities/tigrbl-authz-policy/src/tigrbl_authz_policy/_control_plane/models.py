from __future__ import annotations

from typing import Any, Iterable, Mapping

from tigrbl_identity_contracts.authentication import ServiceIdentityAuthentication
from tigrbl_identity_contracts.authority import Role
from tigrbl_identity_contracts.delegation import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    DelegatedAdminScope,
)
from tigrbl_identity_contracts.policy.conditions import DynamicCondition
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_identity_concrete import ServiceCredential, ServiceIdentity
from tigrbl_authz_policy_concrete import AttributePolicy


def _permission_matches(grant: str, permission: str) -> bool:
    if grant == "*" or grant == permission:
        return True
    if grant.endswith(".*"):
        prefix = grant[:-2]
        return permission == prefix or permission.startswith(f"{prefix}.")
    return False


def _pick_fields(record: Mapping[str, Any], fields: Iterable[str]) -> dict[str, Any]:
    return {field: record[field] for field in fields if field in record}
