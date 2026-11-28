"""W3C WebAuthn wire structures represented with byte-preserving values."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True, slots=True)
class PublicKeyCredentialRpEntity:
    id: str
    name: str


@dataclass(frozen=True, slots=True)
class PublicKeyCredentialUserEntity:
    id: bytes
    name: str
    display_name: str


@dataclass(frozen=True, slots=True)
class PublicKeyCredentialParameters:
    alg: int
    type: str = "public-key"


@dataclass(frozen=True, slots=True)
class PublicKeyCredentialDescriptor:
    id: bytes
    type: str = "public-key"
    transports: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AuthenticatorSelectionCriteria:
    authenticator_attachment: str | None = None
    resident_key: str = "preferred"
    require_resident_key: bool = False
    user_verification: str = "preferred"


@dataclass(frozen=True, slots=True)
class PublicKeyCredentialCreationOptions:
    challenge: bytes
    rp: PublicKeyCredentialRpEntity
    user: PublicKeyCredentialUserEntity
    pub_key_cred_params: tuple[PublicKeyCredentialParameters, ...]
    timeout: int | None = None
    exclude_credentials: tuple[PublicKeyCredentialDescriptor, ...] = ()
    authenticator_selection: AuthenticatorSelectionCriteria | None = None
    attestation: str = "none"
    extensions: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PublicKeyCredentialRequestOptions:
    challenge: bytes
    timeout: int | None = None
    rp_id: str | None = None
    allow_credentials: tuple[PublicKeyCredentialDescriptor, ...] = ()
    user_verification: str = "preferred"
    extensions: Mapping[str, object] = field(default_factory=dict)
    hints: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CollectedClientData:
    type: str
    challenge: str
    origin: str
    cross_origin: bool = False
    top_origin: str | None = None


@dataclass(frozen=True, slots=True)
class AuthenticatorAttestationResponse:
    client_data_json: bytes
    attestation_object: bytes
    transports: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AuthenticatorAssertionResponse:
    client_data_json: bytes
    authenticator_data: bytes
    signature: bytes
    user_handle: bytes | None = None


@dataclass(frozen=True, slots=True)
class PublicKeyCredential:
    id: str
    raw_id: bytes
    response: AuthenticatorAttestationResponse | AuthenticatorAssertionResponse
    type: str = "public-key"
    authenticator_attachment: str | None = None
    client_extension_results: Mapping[str, object] = field(default_factory=dict)


__all__ = [
    "AuthenticatorAssertionResponse",
    "AuthenticatorAttestationResponse",
    "AuthenticatorSelectionCriteria",
    "CollectedClientData",
    "PublicKeyCredential",
    "PublicKeyCredentialCreationOptions",
    "PublicKeyCredentialDescriptor",
    "PublicKeyCredentialParameters",
    "PublicKeyCredentialRequestOptions",
    "PublicKeyCredentialRpEntity",
    "PublicKeyCredentialUserEntity",
]
