"""WebAuthn registration and authentication ceremonies."""

from .authentication import (
    AuthenticationExpectation,
    build_request_options,
    verify_authentication_response,
)
from .registration import (
    RegistrationExpectation,
    build_creation_options,
    verify_registration_response,
)

__all__ = [
    "AuthenticationExpectation",
    "RegistrationExpectation",
    "build_creation_options",
    "build_request_options",
    "verify_authentication_response",
    "verify_registration_response",
]
