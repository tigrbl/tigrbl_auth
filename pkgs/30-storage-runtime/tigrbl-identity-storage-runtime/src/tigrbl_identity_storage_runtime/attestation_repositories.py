from tigrbl_identity_storage.tables.attestation_evidence import AttestationEvidence
from tigrbl_identity_storage.tables.attestation_reference_manifest import (
    AttestationReferenceManifest,
)
from tigrbl_identity_storage.tables.attestation_result import AttestationResult

from .repositories import DurableRepository


class AttestationEvidenceRepository(DurableRepository):
    table = AttestationEvidence
    retained_payload_fields = frozenset(
        {"protected_artifact_locator", "payload_digest"}
    )


class AttestationResultRepository(DurableRepository):
    table = AttestationResult


class AttestationReferenceManifestRepository(DurableRepository):
    table = AttestationReferenceManifest
    retained_payload_fields = frozenset(
        {"protected_artifact_locator", "payload_digest"}
    )


__all__ = [
    "AttestationEvidenceRepository",
    "AttestationReferenceManifestRepository",
    "AttestationResultRepository",
]
