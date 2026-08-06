"""Durable workload-identity lifecycle operations."""

from tigrbl_identity_core.persistence import reject_sensitive_raw_fields
from tigrbl_identity_storage.tables import SpiffeTrustBundle, SvidRecord

from tigrbl import provideTableHandler

record_workload_credential = provideTableHandler(
    SvidRecord, payload_validator=reject_sensitive_raw_fields
)
record_svid = record_workload_credential
activate_spiffe_trust_bundle = provideTableHandler(
    SpiffeTrustBundle, payload_validator=reject_sensitive_raw_fields
)

__all__ = ["activate_spiffe_trust_bundle", "record_svid", "record_workload_credential"]
