"""Durable attestation and reference-material operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from tigrbl_identity_storage.tables import (
    AttestationEndorsement,
    AttestationEvidence,
    AttestationReferenceManifest,
    AttestationReferenceValue,
    AttestationResult,
)

from .common import (
    create_table_handler,
    database_from_context,
    maybe_await,
    payload_from_context,
    reject_sensitive_raw_fields,
)

record_attestation_evidence = create_table_handler(AttestationEvidence)
record_attestation_result = create_table_handler(AttestationResult)


async def publish_reference_material(ctx: Mapping[str, Any]) -> Mapping[str, object]:
    """Stage a manifest and its material in one caller-owned transaction."""

    payload = payload_from_context(ctx)
    reject_sensitive_raw_fields(payload)
    manifest = payload.get("manifest")
    values = payload.get("reference_values", ())
    endorsements = payload.get("endorsements", ())
    if not isinstance(manifest, Mapping):
        raise TypeError("reference material requires a manifest mapping")
    if not isinstance(values, (list, tuple)) or not all(
        isinstance(value, Mapping) for value in values
    ):
        raise TypeError("reference_values must be a sequence of mappings")
    if not isinstance(endorsements, (list, tuple)) or not all(
        isinstance(value, Mapping) for value in endorsements
    ):
        raise TypeError("endorsements must be a sequence of mappings")

    db = database_from_context(ctx)
    manifest_id = manifest.get("manifest_id")
    if not manifest_id:
        raise ValueError("reference manifest requires manifest_id")
    manifest_record = await maybe_await(
        AttestationReferenceManifest.handlers.create.core(
            AttestationReferenceManifest, manifest, db
        )
    )
    value_records = []
    for value in values:
        material = {"manifest_id": manifest_id, **dict(value)}
        value_records.append(
            await maybe_await(
                AttestationReferenceValue.handlers.create.core(
                    AttestationReferenceValue, material, db
                )
            )
        )
    endorsement_records = []
    for endorsement in endorsements:
        endorsement_records.append(
            await maybe_await(
                AttestationEndorsement.handlers.create.core(
                    AttestationEndorsement, endorsement, db
                )
            )
        )
    return {
        "manifest": manifest_record,
        "reference_values": tuple(value_records),
        "endorsements": tuple(endorsement_records),
    }


__all__ = [
    "publish_reference_material",
    "record_attestation_evidence",
    "record_attestation_result",
]
