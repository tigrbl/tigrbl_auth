import hashlib
from tba_contracts_identity.subject_identifiers import (
    SubjectIdentifierKind,
    SubjectIdentifierRequest,
    SubjectIdentifierResult,
)
from tba_bases_identity import SubjectIdentifierStrategyBase


class PairwiseSubjectIdentifierStrategy(SubjectIdentifierStrategyBase):
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult:
        sector = request.sector_identifier or request.issuer
        salt = request.salt or ""
        digest = hashlib.sha256(
            f"{sector}\x1f{request.subject}\x1f{salt}".encode()
        ).hexdigest()
        return SubjectIdentifierResult(digest, SubjectIdentifierKind.PAIRWISE)


__all__ = ["PairwiseSubjectIdentifierStrategy"]
