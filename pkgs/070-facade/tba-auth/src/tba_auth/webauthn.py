"""Stable WebAuthn composition entry points."""

from tba_protocol_webauthn import WebAuthnProtocol
from tba_runtime_identity.composition.webauthn import build_webauthn_composition


def build_webauthn_protocol(
    *, registration, authentication, configuration=None
) -> WebAuthnProtocol:
    return (
        WebAuthnProtocol(registration, authentication, configuration)
        if configuration
        else WebAuthnProtocol(registration, authentication)
    )


def build_webauthn_capabilities(
    *,
    begin_registration,
    complete_registration,
    begin_authentication,
    complete_authentication,
):
    composition = build_webauthn_composition(
        begin_registration=begin_registration,
        complete_registration=complete_registration,
        begin_authentication=begin_authentication,
        complete_authentication=complete_authentication,
    )
    return composition.protocol.registration, composition.protocol.authentication


__all__ = [
    "build_webauthn_capabilities",
    "build_webauthn_protocol",
]
