"""Delegation table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    DelegationGrant,
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantTokenLink,
)

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_delegation_durability.operations.delegation import (
    activate_grant,
    create_grant,
    deactivate_grant_children,
    expire_grant,
    inspect_grant,
    link_delegation_token,
    link_grant_edge,
    list_grants,
    list_tokens_for_grant,
    persist_delegation_provenance,
    replace_grant,
    revoke_grant,
)


DelegationGrantTable = DelegationGrant
DelegationGrantEdgeTable = DelegationGrantEdge
DelegationGrantProofTable = DelegationGrantProof
DelegationGrantTokenLinkTable = DelegationGrantTokenLink

DelegationGrantRuntimeSpec = deriveRuntimeTableSpec(
    DelegationGrantTable,
    operations=tuple(
        makeRuntimeOperation(alias=alias, handler=handler)
        for alias, handler in (
            ("create_grant", create_grant),
            ("inspect_grant", inspect_grant),
            ("list_grants", list_grants),
            ("activate_grant", activate_grant),
            ("expire_grant", expire_grant),
            ("replace_grant", replace_grant),
            ("revoke_grant", revoke_grant),
        )
    ),
)
DelegationGrantEdgeRuntimeSpec = deriveRuntimeTableSpec(
    DelegationGrantEdgeTable,
    operations=(
        makeRuntimeOperation(alias="link_edge", handler=link_grant_edge),
        makeRuntimeOperation(
            alias="deactivate_children",
            handler=deactivate_grant_children,
        ),
    ),
)
DelegationGrantProofRuntimeSpec = deriveRuntimeTableSpec(
    DelegationGrantProofTable,
    operations=(
        makeRuntimeOperation(
            alias="persist_provenance",
            handler=persist_delegation_provenance,
        ),
    ),
)
DelegationGrantTokenLinkRuntimeSpec = deriveRuntimeTableSpec(
    DelegationGrantTokenLinkTable,
    operations=(
        makeRuntimeOperation(alias="link_token", handler=link_delegation_token),
        makeRuntimeOperation(alias="list_for_grant", handler=list_tokens_for_grant),
    ),
)


__all__ = [
    "DelegationGrantEdgeRuntimeSpec",
    "DelegationGrantEdgeTable",
    "DelegationGrantProofRuntimeSpec",
    "DelegationGrantProofTable",
    "DelegationGrantRuntimeSpec",
    "DelegationGrantTable",
    "DelegationGrantTokenLinkRuntimeSpec",
    "DelegationGrantTokenLinkTable",
]
