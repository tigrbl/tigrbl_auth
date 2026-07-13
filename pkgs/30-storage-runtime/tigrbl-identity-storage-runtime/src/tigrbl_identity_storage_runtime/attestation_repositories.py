from tigrbl_identity_storage.tables.attestation_evidence import AttestationEvidence
from tigrbl_identity_storage.tables.attestation_reference_manifest import (
    AttestationReferenceManifest,
)
from tigrbl_identity_storage.tables.attestation_result import AttestationResult
from tigrbl_identity_storage.tables.attestation_reference_value import AttestationReferenceValue
from tigrbl_identity_storage.tables.attestation_endorsement import AttestationEndorsement
from tigrbl_identity_contracts.attestation import ReferenceIntegrityManifest

from .repositories import AsyncRecordStore, AsyncTransactionManager, DurableRepository, StorageTransactionCoordinator


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


class AttestationReferenceValueRepository(DurableRepository):
    table = AttestationReferenceValue


class AttestationEndorsementRepository(DurableRepository):
    table = AttestationEndorsement
    retained_payload_fields = frozenset({"artifact_locator", "artifact_digest"})


class CorimReferenceMaterialRepository:
    """Atomic immutable publication of CoRIM/CoMID reference material."""

    provider_id = "corim-reference:sql"
    persistence = "durable"

    def __init__(self, store: AsyncRecordStore, transactions: AsyncTransactionManager):
        self._manifests = AttestationReferenceManifestRepository(store)
        self._values = AttestationReferenceValueRepository(store)
        self._endorsements = AttestationEndorsementRepository(store)
        self._transactions = StorageTransactionCoordinator(transactions)

    async def publish(
        self,
        manifest: ReferenceIntegrityManifest,
        *,
        artifact_locator: str,
        artifact_digest: str,
        profile: str,
        reference_values: tuple[dict[str, object], ...] = (),
        endorsements: tuple[dict[str, object], ...] = (),
    ) -> object:
        if not artifact_locator or not artifact_digest or not profile:
            raise ValueError("artifact locator, digest, and CoRIM profile are required")
        async with self._transactions.transaction():
            existing = await self._manifests.find(manifest_id=manifest.tag_identity)
            if existing:
                raise ValueError(
                    f"CoRIM reference manifest is immutable once published: {manifest.tag_identity}"
                )
            row = await self._manifests.create(
                manifest_id=manifest.tag_identity,
                profile=profile,
                format="corim",
                artifact_locator=artifact_locator,
                artifact_digest=artifact_digest,
                signer=manifest.signer,
            )
            for value in reference_values:
                await self._values.create(manifest_id=manifest.tag_identity, **value)
            for endorsement in endorsements:
                await self._endorsements.create(profile=profile, **endorsement)
            return row


__all__ = [
    "AttestationEvidenceRepository",
    "AttestationReferenceManifestRepository",
    "AttestationReferenceValueRepository",
    "AttestationEndorsementRepository",
    "AttestationResultRepository",
    "CorimReferenceMaterialRepository",
]
