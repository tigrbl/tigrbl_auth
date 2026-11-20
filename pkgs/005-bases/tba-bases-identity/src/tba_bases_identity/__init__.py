"""Protocol-neutral identity bases."""

from abc import ABC

from tba_contracts_identity.principals import Identity
from tba_contracts_identity.subject_identifiers import (
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
