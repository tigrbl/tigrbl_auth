"""Reportable WebAuthn protocol surface."""

from __future__ import annotations

from dataclasses import dataclass

from tigrbl_public_key_authentication_capability import (
    PublicKeyAuthenticationCapability,
)
from tigrbl_public_key_registration_capability import PublicKeyRegistrationCapability

from .bindings import CAPABILITY_REQUIREMENTS
from .configuration import WebAuthnConfiguration
from .features import features_for
from .versions import CURRENT_VERSION


@dataclass(frozen=True, slots=True)
class WebAuthnProtocol:
    registration: PublicKeyRegistrationCapability
    authentication: PublicKeyAuthenticationCapability
    configuration: WebAuthnConfiguration = WebAuthnConfiguration()

    def capability_report(self) -> dict[str, object]:
        return {
            "protocol": "webauthn",
            "revision": CURRENT_VERSION.identifier,
            "supported_features": tuple(
                sorted(features_for(self.configuration.version))
            ),
            "enabled_features": tuple(sorted(self.configuration.enabled_features)),
            "requirements": CAPABILITY_REQUIREMENTS,
            "capabilities": {
                "registration": self.registration.capability_report(),
                "authentication": self.authentication.capability_report(),
            },
        }


__all__ = ["WebAuthnProtocol"]
