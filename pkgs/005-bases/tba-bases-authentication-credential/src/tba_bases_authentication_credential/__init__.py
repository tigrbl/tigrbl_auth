"""Protocol-neutral authentication-credential bases."""

from tba_contracts_identity.credentials import Credential


class CredentialBase(Credential):
    """Base for concrete authentication credential variants."""


__all__ = ["CredentialBase"]
