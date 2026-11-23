from __future__ import annotations

from tba_contracts_identity.oidc import SubjectIdentifierRequest, SubjectIdentifierResult
from tba_concrete_pairwise_subject_identifier import (
    PairwiseSubjectIdentifierStrategy,
)

from tba_contracts_security_trust import CapabilityMap
from tba_bases_identity import SubjectIdentifierStrategyBase

PairwiseSubjectStrategy = PairwiseSubjectIdentifierStrategy


class PairwiseSubjectProvider(SubjectIdentifierStrategyBase):
    def __init__(self, strategy: PairwiseSubjectStrategy | None = None) -> None:
        self._strategy = strategy or PairwiseSubjectStrategy()

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"derive_subject": ("pairwise",)}, features=("oidc-subject", "pairwise"))

    def derive(self, request: SubjectIdentifierRequest) -> SubjectIdentifierResult:
        return self._strategy.derive(request)


__all__ = ["PairwiseSubjectProvider"]
