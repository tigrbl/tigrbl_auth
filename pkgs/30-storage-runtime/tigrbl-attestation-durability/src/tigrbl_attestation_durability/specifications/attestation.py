"""Attestation table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    AttestationEvidence,
    AttestationReferenceManifest,
    AttestationResult,
)

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_attestation_durability.operations.attestation import (
    publish_reference_material,
    record_attestation_evidence,
    record_attestation_result,
)

AttestationEvidenceTable = AttestationEvidence
AttestationResultTable = AttestationResult
AttestationReferenceManifestTable = AttestationReferenceManifest

AttestationEvidenceRuntimeSpec = deriveRuntimeTableSpec(
    AttestationEvidenceTable,
    operations=(
        makeRuntimeOperation(
            alias="record_evidence", handler=record_attestation_evidence
        ),
    ),
)
AttestationResultRuntimeSpec = deriveRuntimeTableSpec(
    AttestationResultTable,
    operations=(
        makeRuntimeOperation(
            alias="record_appraisal_result", handler=record_attestation_result
        ),
    ),
)
AttestationReferenceManifestRuntimeSpec = deriveRuntimeTableSpec(
    AttestationReferenceManifestTable,
    operations=(
        makeRuntimeOperation(
            alias="publish_reference_material",
            handler=publish_reference_material,
        ),
    ),
)

__all__ = [
    "AttestationEvidenceRuntimeSpec",
    "AttestationEvidenceTable",
    "AttestationReferenceManifestRuntimeSpec",
    "AttestationReferenceManifestTable",
    "AttestationResultRuntimeSpec",
    "AttestationResultTable",
]
