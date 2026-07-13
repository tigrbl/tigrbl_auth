from collections.abc import Callable

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityMetadata
from tigrbl_identity_contracts.attestation import (
    AppraisalResult,
    AttestationAppraiserPort,
    AttestationEvidence,
)

ResultRecorder = Callable[[AttestationEvidence, AppraisalResult], None]


class AttestationAppraisalCapability(Capability):
    def __init__(
        self,
        appraiser: AttestationAppraiserPort,
        recorder: ResultRecorder | None = None,
    ):
        super().__init__(
            CapabilityMetadata(
                capability_id="attestation.appraisal",
                version="1.0",
                operations=("appraise",),
                guarantees=("appraisal-before-recording",),
                dependencies=(type(appraiser).__name__,),
            )
        )
        self._appraiser = appraiser
        self._recorder = recorder
        self.bind("appraise", self.appraise, delegated=True)

    def appraise(self, evidence: AttestationEvidence) -> AppraisalResult:
        result = self._appraiser.appraise(evidence)
        if self._recorder is not None:
            self._recorder(evidence, result)
        return result


__all__ = ["AttestationAppraisalCapability", "ResultRecorder"]
