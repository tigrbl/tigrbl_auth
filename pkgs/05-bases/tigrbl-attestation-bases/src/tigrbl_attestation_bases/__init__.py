from abc import ABC

from tigrbl_identity_contracts.attestation import (
    AppraisalResult,
    AttestationAppraiserPort,
    AttestationEvidence,
    EvidenceVerificationResult,
    EvidenceVerifierPort,
    ReferenceIntegrityManifest,
    ReferenceMaterialProviderPort,
    VerifiedAttestationEvidence,
)


class EvidenceVerifierBase(EvidenceVerifierPort, ABC):
    def verify_evidence(
        self, evidence: AttestationEvidence, /
    ) -> EvidenceVerificationResult:
        raise NotImplementedError


class AttestationAppraiserBase(AttestationAppraiserPort, ABC):
    def appraise(
        self, evidence: VerifiedAttestationEvidence, /
    ) -> AppraisalResult:
        raise NotImplementedError


class ReferenceMaterialProviderBase(ReferenceMaterialProviderPort, ABC):
    def resolve_manifest(self, tag_identity: str, /) -> ReferenceIntegrityManifest:
        raise NotImplementedError


class ReferenceManifestBase(ABC):
    """Common extension point for CoRIM-family and other reference manifests."""


__all__ = [
    "AttestationAppraiserBase",
    "EvidenceVerifierBase",
    "ReferenceManifestBase",
    "ReferenceMaterialProviderBase",
]
