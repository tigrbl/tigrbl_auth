"""Map WebAuthn wire ceremonies to stable semantic capability operations."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "webauthn",
        CURRENT_VERSION.identifier,
        "webauthn-registration-begin",
        "PublicKeyCredentialCreationOptions",
        "credential.public-key.registration",
        "begin_public_key_registration",
        "public-key-registration-options",
    ),
    ProtocolCapabilityRequirement(
        "webauthn",
        CURRENT_VERSION.identifier,
        "webauthn-registration-complete",
        "AuthenticatorAttestationResponse",
        "credential.public-key.registration",
        "complete_public_key_registration",
        "verified-public-key-registration",
    ),
    ProtocolCapabilityRequirement(
        "webauthn",
        CURRENT_VERSION.identifier,
        "webauthn-authentication-begin",
        "PublicKeyCredentialRequestOptions",
        "credential.public-key.authentication",
        "begin_public_key_authentication",
        "public-key-authentication-options",
    ),
    ProtocolCapabilityRequirement(
        "webauthn",
        CURRENT_VERSION.identifier,
        "webauthn-authentication-complete",
        "AuthenticatorAssertionResponse",
        "credential.public-key.authentication",
        "complete_public_key_authentication",
        "verified-public-key-assertion",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
