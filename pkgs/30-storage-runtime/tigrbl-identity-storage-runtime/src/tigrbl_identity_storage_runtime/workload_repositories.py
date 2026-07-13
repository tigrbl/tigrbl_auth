from tigrbl_identity_storage.tables.spiffe_trust_bundle import SpiffeTrustBundle
from tigrbl_identity_storage.tables.svid_record import SvidRecord

from .repositories import DurableRepository


class SvidRecordRepository(DurableRepository):
    table = SvidRecord
    retained_payload_fields = frozenset(
        {"protected_artifact_locator", "payload_digest"}
    )


class SpiffeTrustBundleRepository(DurableRepository):
    table = SpiffeTrustBundle
    retained_payload_fields = frozenset(
        {"protected_artifact_locator", "payload_digest"}
    )


__all__ = ["SpiffeTrustBundleRepository", "SvidRecordRepository"]
