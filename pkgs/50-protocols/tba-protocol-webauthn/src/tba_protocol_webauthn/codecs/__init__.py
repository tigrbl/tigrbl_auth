"""Binary codecs used by WebAuthn ceremonies."""

from .attestation_object import AttestationObject, decode_attestation_object
from .authenticator_data import (
    AttestedCredentialData,
    AuthenticatorData,
    AuthenticatorDataFlags,
    decode_authenticator_data,
)
from .client_data import ParsedClientData, parse_client_data
from .credential_public_key import decode_credential_public_key

__all__ = [
    "AttestationObject",
    "AttestedCredentialData",
    "AuthenticatorData",
    "AuthenticatorDataFlags",
    "ParsedClientData",
    "decode_attestation_object",
    "decode_authenticator_data",
    "decode_credential_public_key",
    "parse_client_data",
]
