"""Durable workload-identity lifecycle operations."""

from tigrbl_identity_storage.tables import SpiffeTrustBundle, SvidRecord

from .common import create_table_handler

record_svid = create_table_handler(SvidRecord)
activate_spiffe_trust_bundle = create_table_handler(SpiffeTrustBundle)

__all__ = ["activate_spiffe_trust_bundle", "record_svid"]
