from __future__ import annotations

from tigrbl_identity_contracts.oidc import SubjectIdentifierRequest, SubjectIdentifierResult
from tigrbl_pairwise_subject_identifier_concrete import (
    PairwiseSubjectIdentifierStrategy,
)

from tigrbl_security_trust_contracts import CapabilityMap
from tigrbl_identity_model_bases import SubjectIdentifierStrategyBase

PairwiseSubjectStrategy = PairwiseSubjectIdentifierStrategy


class PairwiseSubjectProvider(SubjectIdentifierStrategyBase):
    def __init__(self, strategy: PairwiseSubjectStrategy | None = None) -> None:
        self._strategy = strategy or PairwiseSubjectStrategy()

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"derive_subject": ("pairwise",)}, features=("oidc-subject", "pairwise"))

    def derive(self, request: SubjectIdentifierRequest) -> SubjectIdentifierResult:
        return self._strategy.derive(request)


__all__ = ["PairwiseSubjectProvider"]
