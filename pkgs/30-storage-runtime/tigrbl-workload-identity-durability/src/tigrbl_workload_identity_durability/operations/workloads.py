"""Durable workload-identity lifecycle operations."""

from tigrbl_identity_storage.tables import SpiffeTrustBundle, SvidRecord

from tigrbl_table_durability import create_table_handler

record_workload_credential = create_table_handler(SvidRecord)
record_svid = record_workload_credential
activate_spiffe_trust_bundle = create_table_handler(SpiffeTrustBundle)

__all__ = ["activate_spiffe_trust_bundle", "record_svid", "record_workload_credential"]
