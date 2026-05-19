"""Executable RPC method modules for the implementation-backed admin plane."""

from .audit import METHODS as AUDIT_METHODS
from .client_registration import METHODS as CLIENT_REGISTRATION_METHODS
from .consent import METHODS as CONSENT_METHODS
from .directory import METHODS as DIRECTORY_METHODS
from .governance import METHODS as GOVERNANCE_METHODS
from .keys import METHODS as KEY_METHODS
from .profile import METHODS as PROFILE_METHODS
from .session import METHODS as SESSION_METHODS
from .token import METHODS as TOKEN_METHODS

METHODS = (
    *GOVERNANCE_METHODS,
    *DIRECTORY_METHODS,
    *CLIENT_REGISTRATION_METHODS,
    *SESSION_METHODS,
    *TOKEN_METHODS,
    *CONSENT_METHODS,
    *AUDIT_METHODS,
    *KEY_METHODS,
    *PROFILE_METHODS,
)

__all__ = ["METHODS"]
