"""Protocol-neutral identity bases."""

from abc import ABC

from tigrbl_identity_contracts.principals import Identity
from tigrbl_identity_contracts.subject_identifiers import (
    SubjectIdentifierRequest,
    SubjectIdentifierResult,
    SubjectIdentifierStrategyPort,
)


class SubjectIdentifierStrategyBase(SubjectIdentifierStrategyPort, ABC):
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult:
        raise NotImplementedError


class IdentityBase(Identity):
    """Base for concrete identity variants."""


__all__ = ["IdentityBase", "SubjectIdentifierStrategyBase"]
