class WebAuthnProtocolError(ValueError):
    """Base WebAuthn parsing and verification failure."""


class WebAuthnVerificationError(WebAuthnProtocolError):
    """A supplied WebAuthn artifact failed a binding or verification rule."""


class ClientDataError(WebAuthnProtocolError):
    pass


class AuthenticatorDataError(WebAuthnProtocolError):
    pass


class AttestationObjectError(WebAuthnProtocolError):
    pass


class RegistrationVerificationError(WebAuthnProtocolError):
    pass


class AuthenticationVerificationError(WebAuthnProtocolError):
    pass


__all__ = [name for name in globals() if name.endswith("Error")]
