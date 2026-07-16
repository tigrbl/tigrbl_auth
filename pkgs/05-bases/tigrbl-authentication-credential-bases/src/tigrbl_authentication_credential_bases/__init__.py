"""Protocol-neutral authentication-credential bases."""

from tigrbl_identity_contracts.credentials import Credential


class CredentialBase(Credential):
    """Base for concrete authentication credential variants."""


__all__ = ["CredentialBase"]
