"""Workload reference and entitlement table runtime specifications."""

from tigrbl_identity_storage.tables import (
    WorkloadCredentialEntitlement,
    WorkloadReferenceBinding,
)
from tigrbl import deriveTableSpec, makeOp
from tigrbl_workload_identity_durability.operations.references import (
    bind_workload_reference,
    grant_workload_credential_entitlement,
)

WorkloadReferenceBindingTable = WorkloadReferenceBinding
WorkloadCredentialEntitlementTable = WorkloadCredentialEntitlement
WorkloadReferenceBindingRuntimeSpec = deriveTableSpec(
    WorkloadReferenceBindingTable,
    ops=(
        makeOp(
            extra={"owner_layer": "30-storage-runtime"},
            expose_routes=False,
            expose_rpc=False,
            expose_method=True,
            tx_scope="read_write",
            alias="bind_workload_reference",
            handler=bind_workload_reference,
        ),
    ),
)
WorkloadCredentialEntitlementRuntimeSpec = deriveTableSpec(
    WorkloadCredentialEntitlementTable,
    ops=(
        makeOp(
            extra={"owner_layer": "30-storage-runtime"},
            expose_routes=False,
            expose_rpc=False,
            expose_method=True,
            tx_scope="read_write",
            alias="grant_workload_credential_entitlement",
            handler=grant_workload_credential_entitlement,
        ),
    ),
)
__all__ = [
    "WorkloadCredentialEntitlementRuntimeSpec",
    "WorkloadCredentialEntitlementTable",
    "WorkloadReferenceBindingRuntimeSpec",
    "WorkloadReferenceBindingTable",
]
