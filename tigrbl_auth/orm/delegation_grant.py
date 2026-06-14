"""Compatibility facade for DelegationGrant lifecycle ORM imports."""

from tigrbl_auth.tables.delegation_grant import (
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantRecord,
    DelegationGrantScope,
    DelegationGrantTokenLink,
)

__all__ = [
    "DelegationGrantEdge",
    "DelegationGrantProof",
    "DelegationGrantRecord",
    "DelegationGrantScope",
    "DelegationGrantTokenLink",
]
