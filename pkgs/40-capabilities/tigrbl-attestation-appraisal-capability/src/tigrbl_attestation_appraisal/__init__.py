import inspect
from collections.abc import Callable

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)
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

ResultRecorder = Callable[[VerifiedAttestationEvidence, AppraisalResult], object]


class AttestationAppraisalCapability(Capability):
    def __init__(
        self,
        verifier: EvidenceVerifierPort,
        appraiser: AttestationAppraiserPort,
        reference_provider: ReferenceMaterialProviderPort | None = None,
        recorder: ResultRecorder | None = None,
    ):
        super().__init__(
            CapabilityDefinition(
                capability_id="attestation.appraisal",
                version="1.0",
            ),
            operations={
                "verify_evidence": CapabilityOperation(
                    target=self.verify_evidence,
                    delegated=True,
                ),
                "resolve_reference_material": CapabilityOperation(
                    target=(
                        self.resolve_reference_material
                        if reference_provider is not None
                        else None
                    ),
                    required=False,
                    delegated=True,
                ),
                "appraise": CapabilityOperation(
                    target=self.appraise,
                    delegated=True,
                ),
                "record_result": CapabilityOperation(
                    target=self.record_result if recorder is not None else None,
                    required=False,
                    delegated=True,
                ),
            },
        )
        self._verifier = verifier
        self._appraiser = appraiser
        self._reference_provider = reference_provider
        self._recorder = recorder

    def verify_evidence(
        self, evidence: AttestationEvidence
    ) -> EvidenceVerificationResult:
        return self._verifier.verify_evidence(evidence)

    def resolve_reference_material(
        self, tag_identity: str
    ) -> ReferenceIntegrityManifest:
        if self._reference_provider is None:
            raise LookupError("reference material provider is not configured")
        return self._reference_provider.resolve_manifest(tag_identity)

    async def record_result(
        self,
        evidence: VerifiedAttestationEvidence,
        result: AppraisalResult,
    ) -> object:
        if self._recorder is None:
            raise LookupError("attestation result recorder is not configured")
        recorded = self._recorder(evidence, result)
        if inspect.isawaitable(recorded):
            recorded = await recorded
        return recorded

    async def appraise(self, evidence: AttestationEvidence) -> AppraisalResult:
        verification = self.verify_evidence(evidence)
        if not verification.verified or verification.evidence is None:
            return AppraisalResult(
                False, f"evidence verification failed: {verification.reason}"
            )
        result = self._appraiser.appraise(verification.evidence)
        if self._recorder is not None:
            await self.record_result(verification.evidence, result)
        return result


__all__ = ["AttestationAppraisalCapability", "ResultRecorder"]
