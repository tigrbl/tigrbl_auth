from __future__ import annotations

import hashlib

from tigrbl_identity_contracts.oidc import (
    SubjectIdentifierKind,
    SubjectIdentifierRequest,
    SubjectIdentifierResult,
)


class PublicSubjectStrategy:
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult:
        return SubjectIdentifierResult(str(request.subject), SubjectIdentifierKind.PUBLIC)


class PairwiseSubjectStrategy:
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult:
        sector = request.sector_identifier or request.issuer
        salt = request.salt or ""
        digest = hashlib.sha256(f"{sector}\x1f{request.subject}\x1f{salt}".encode("utf-8")).hexdigest()
        return SubjectIdentifierResult(digest, SubjectIdentifierKind.PAIRWISE)


__all__ = ["PairwiseSubjectStrategy", "PublicSubjectStrategy"]
