"""Base classes for concrete identity and credential models."""

from tigrbl_identity_contracts.credentials import Credential
from tigrbl_identity_contracts.principals import Identity

from .artifacts import (
    ArtifactVerifierBase,
    CredentialIssuerBase,
    PresentationBuilderBase,
)
from .normalization import clean_mapping, clean_tuple, new_model_id, required_text


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
]
