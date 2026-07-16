from tigrbl_identity_contracts.subject_identifiers import (
    SubjectIdentifierKind,
    SubjectIdentifierRequest,
    SubjectIdentifierResult,
)
from tigrbl_identity_bases import SubjectIdentifierStrategyBase


class PublicSubjectIdentifierStrategy(SubjectIdentifierStrategyBase):
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult:
        return SubjectIdentifierResult(
            str(request.subject), SubjectIdentifierKind.PUBLIC
        )


__all__ = ["PublicSubjectIdentifierStrategy"]
