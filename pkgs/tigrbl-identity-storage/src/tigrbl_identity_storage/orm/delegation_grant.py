"""ORM import facade for DelegationGrant lifecycle tables."""

from tigrbl_identity_storage.tables.delegation_grant import (
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
