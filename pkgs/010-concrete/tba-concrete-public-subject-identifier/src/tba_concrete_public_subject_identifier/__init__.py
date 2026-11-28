from tba_contracts_identity.subject_identifiers import (
    SubjectIdentifierKind,
    SubjectIdentifierRequest,
    SubjectIdentifierResult,
)
from tba_bases_identity import SubjectIdentifierStrategyBase


class PublicSubjectIdentifierStrategy(SubjectIdentifierStrategyBase):
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult:
        return SubjectIdentifierResult(
            str(request.subject), SubjectIdentifierKind.PUBLIC
        )


__all__ = ["PublicSubjectIdentifierStrategy"]
