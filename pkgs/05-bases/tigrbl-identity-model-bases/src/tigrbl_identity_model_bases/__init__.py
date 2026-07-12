"""Base classes for concrete identity and credential models."""

from tigrbl_identity_contracts.credentials import Credential
from tigrbl_identity_contracts.principals import Identity

from .artifacts import (
    ArtifactVerifierBase,
    CredentialIssuerBase,
    PresentationBuilderBase,
)
from .normalization import clean_mapping, clean_tuple, new_model_id, required_text
from abc import ABC
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


class CredentialBase(Credential):
    """Base for concrete credential variants."""


__all__ = [
    "ArtifactVerifierBase",
    "CredentialBase",
    "CredentialIssuerBase",
    "IdentityBase",
    "PresentationBuilderBase",
    "clean_mapping",
    "clean_tuple",
    "new_model_id",
    "required_text",
    "SubjectIdentifierStrategyBase",
]
