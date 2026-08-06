"""Durable workload-reference and credential-entitlement operations."""

from tigrbl_identity_core.persistence import reject_sensitive_raw_fields
from tigrbl_identity_storage.tables import (
    WorkloadCredentialEntitlement,
    WorkloadReferenceBinding,
)
from tigrbl import provideTableHandler

bind_workload_reference = provideTableHandler(
    WorkloadReferenceBinding, payload_validator=reject_sensitive_raw_fields
)
grant_workload_credential_entitlement = provideTableHandler(
    WorkloadCredentialEntitlement, payload_validator=reject_sensitive_raw_fields
)
__all__ = ["bind_workload_reference", "grant_workload_credential_entitlement"]
