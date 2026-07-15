from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "fido2-server",
        CURRENT_VERSION.identifier,
        "registration",
        "WebAuthn registration",
        "credential.public-key.registration",
        "complete_public_key_registration",
        "verified-public-key-registration",
    ),
    ProtocolCapabilityRequirement(
        "fido2-server",
        CURRENT_VERSION.identifier,
        "authentication",
        "WebAuthn assertion",
        "credential.public-key.authentication",
        "complete_public_key_authentication",
        "verified-public-key-assertion",
    ),
    ProtocolCapabilityRequirement(
        "fido2-server",
        CURRENT_VERSION.identifier,
        "metadata",
        "AAGUID metadata",
        "authenticator.attestation",
        "resolve_authenticator_metadata",
        "authenticator-metadata",
        required=False,
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
