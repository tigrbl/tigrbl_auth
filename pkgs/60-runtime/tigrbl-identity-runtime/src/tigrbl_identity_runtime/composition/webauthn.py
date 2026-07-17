"""Composition root for the independently mountable WebAuthn slices."""

from __future__ import annotations

from dataclasses import dataclass

from tigrbl_auth_protocol_webauthn import WebAuthnConfiguration, WebAuthnProtocol
from tigrbl_public_key_authentication_capability import (
    PublicKeyAuthenticationCapability,
)
from tigrbl_public_key_credential_management_capability import (
    PublicKeyCredentialManagementCapability,
)
from tigrbl_public_key_registration_capability import PublicKeyRegistrationCapability


@dataclass(frozen=True, slots=True)
class WebAuthnComposition:
    protocol: WebAuthnProtocol
    credential_management: PublicKeyCredentialManagementCapability | None


def build_webauthn_composition(
    *,
    begin_registration,
    complete_registration,
    begin_authentication,
    complete_authentication,
    list_credentials=None,
    rename_credential=None,
    revoke_credential=None,
    configuration: WebAuthnConfiguration | None = None,
) -> WebAuthnComposition:
    registration = PublicKeyRegistrationCapability(
        begin_registration, complete_registration
    )
    authentication = PublicKeyAuthenticationCapability(
        begin_authentication, complete_authentication
    )
    management = None
    if list_credentials and rename_credential and revoke_credential:
        management = PublicKeyCredentialManagementCapability(
            list_credentials=list_credentials,
            rename_credential=rename_credential,
            revoke_credential=revoke_credential,
        )
    protocol = WebAuthnProtocol(
        registration, authentication, configuration or WebAuthnConfiguration()
    )
    return WebAuthnComposition(protocol, management)


__all__ = ["WebAuthnComposition", "build_webauthn_composition"]
