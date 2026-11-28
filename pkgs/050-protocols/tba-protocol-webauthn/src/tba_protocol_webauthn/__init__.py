"""Versioned W3C Web Authentication relying-party protocol."""

from .attestation import (
    AttestationVerificationInput,
    AttestationVerifierRegistry,
    build_attestation_registry,
)
from .bindings import CAPABILITY_REQUIREMENTS
from .ceremonies import (
    AuthenticationExpectation,
    RegistrationExpectation,
    build_creation_options,
    build_request_options,
    verify_authentication_response,
    verify_registration_response,
)
from .claims import CLAIM_NAMES
from .codecs import (
    AttestationObject,
    AttestedCredentialData,
    AuthenticatorData,
    AuthenticatorDataFlags,
    ParsedClientData,
    decode_attestation_object,
    decode_authenticator_data,
    decode_credential_public_key,
    parse_client_data,
)
from .compatibility import compatible_features
from .configuration import WebAuthnConfiguration
from .errors import (
    AuthenticationVerificationError,
    AttestationObjectError,
    AuthenticatorDataError,
    ClientDataError,
    RegistrationVerificationError,
    WebAuthnProtocolError,
    WebAuthnVerificationError,
)
from .extensions import (
    ExtensionRegistry,
    validate_appid,
    validate_cred_props,
    validate_credential_protection,
    validate_large_blob,
    validate_payment,
)
from .features import BASE_FEATURES, LEVEL_3_FEATURES, WebAuthnFeature, features_for
from .migrations import migration_path
from .protocol import WebAuthnProtocol
from .related_origins import origin_is_allowed
from .schemas import (
    AuthenticatorAssertionResponse,
    AuthenticatorAttestationResponse,
    AuthenticatorSelectionCriteria,
    CollectedClientData,
    PublicKeyCredential,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialParameters,
    PublicKeyCredentialRequestOptions,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
)
from .versions import (
    CURRENT_VERSION,
    WEB_AUTHN_REVISIONS,
    WebAuthnRevision,
    WebAuthnVersion,
    resolve_revision,
)

__all__ = [
    "AttestationObject",
    "AttestationVerificationInput",
    "AttestationVerifierRegistry",
    "AttestedCredentialData",
    "AuthenticationExpectation",
    "AuthenticationVerificationError",
    "AuthenticatorAssertionResponse",
    "AuthenticatorAttestationResponse",
    "AuthenticatorData",
    "AuthenticatorDataError",
    "AuthenticatorDataFlags",
    "AuthenticatorSelectionCriteria",
    "BASE_FEATURES",
    "CAPABILITY_REQUIREMENTS",
    "CLAIM_NAMES",
    "CURRENT_VERSION",
    "ClientDataError",
    "CollectedClientData",
    "ExtensionRegistry",
    "LEVEL_3_FEATURES",
    "ParsedClientData",
    "PublicKeyCredential",
    "PublicKeyCredentialCreationOptions",
    "PublicKeyCredentialDescriptor",
    "PublicKeyCredentialParameters",
    "PublicKeyCredentialRequestOptions",
    "PublicKeyCredentialRpEntity",
    "PublicKeyCredentialUserEntity",
    "RegistrationExpectation",
    "RegistrationVerificationError",
    "WEB_AUTHN_REVISIONS",
    "WebAuthnConfiguration",
    "WebAuthnFeature",
    "WebAuthnProtocol",
    "WebAuthnProtocolError",
    "WebAuthnRevision",
    "WebAuthnVerificationError",
    "WebAuthnVersion",
    "build_attestation_registry",
    "build_creation_options",
    "build_request_options",
    "compatible_features",
    "decode_attestation_object",
    "decode_authenticator_data",
    "decode_credential_public_key",
    "features_for",
    "migration_path",
    "origin_is_allowed",
    "parse_client_data",
    "resolve_revision",
    "validate_appid",
    "validate_cred_props",
    "validate_credential_protection",
    "validate_large_blob",
    "validate_payment",
    "verify_authentication_response",
    "verify_registration_response",
]
