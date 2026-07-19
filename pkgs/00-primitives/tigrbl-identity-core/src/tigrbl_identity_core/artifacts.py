"""Dependency-light taxonomy for identity and security artifacts."""

from enum import Enum


class ArtifactKind(str, Enum):
    CREDENTIAL = "credential"
    TOKEN = "token"
    PRESENTATION = "presentation"
    ATTESTATION = "attestation"
    MANIFEST = "manifest"
    CERTIFICATE = "certificate"
    IDENTITY_DOCUMENT = "identity-document"
    PROTECTED_ENVELOPE = "protected-envelope"
    STATUS = "status"


class CredentialFormat(str, Enum):
    W3C_VCDM = "w3c-vcdm"
    SD_JWT_VC = "sd-jwt-vc"
    ISO_MDOC = "iso-mdoc"
    X509 = "x509"
    X509_SVID = "x509-svid"
    JWT_SVID = "jwt-svid"
    WIT = "wit"
    WIT_SVID = "wit-svid"
    CWT_SVID_EXTENSION = "cwt-svid-extension"
    VC_JOSE = "vc-jose"
    VC_COSE = "vc-cose"


class TokenKind(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    ID = "id"
    SECURITY_EVENT = "security-event"
    ENTITY_ATTESTATION = "entity-attestation"
    WORKLOAD_IDENTITY = "workload-identity"
    PROOF = "proof"
    CONTINUATION = "continuation"
    JWT = "jwt"
    CWT = "cwt"
    OIDC_ID_TOKEN = "oidc-id-token"
    JWT_SVID = "jwt-svid"
    WORKLOAD_IDENTITY_TOKEN = "workload-identity-token"
    WORKLOAD_PROOF_TOKEN = "workload-proof-token"
    CWT_SVID_EXTENSION = "cwt-svid-extension"


class PresentationKind(str, Enum):
    W3C_VP = "w3c-vp"
    SD_JWT = "sd-jwt"
    ISO_MDOC = "iso-mdoc"
    VC_JOSE = "vc-jose"
    VC_COSE = "vc-cose"
    WORKLOAD_AUTHENTICATION = "workload-authentication"


class IdentityDocumentKind(str, Enum):
    DID_DOCUMENT = "did-document"
    SPIFFE_SVID = "spiffe-svid"


class ProtectedEnvelopeKind(str, Enum):
    JWS = "jws"
    JWE = "jwe"
    COSE_SIGN = "cose-sign"
    COSE_SIGN1 = "cose-sign1"
    COSE_ENCRYPT = "cose-encrypt"
    COSE_ENCRYPT0 = "cose-encrypt0"
    COSE_MAC = "cose-mac"
    COSE_MAC0 = "cose-mac0"


class AttestationKind(str, Enum):
    ENTITY = "entity"
    WALLET = "wallet"
    KEY = "key"
    PLATFORM = "platform"


class ManifestKind(str, Enum):
    CORIM = "corim"
    COMID = "comid"
    COSWID = "coswid"
    COTL = "cotl"
    COTS = "cots"
    TRUST_BUNDLE = "trust-bundle"
    STATUS_LIST = "status-list"


class VerificationOutcome(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    INDETERMINATE = "indeterminate"


class LifecycleStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"


__all__ = [
    "ArtifactKind",
    "AttestationKind",
    "CredentialFormat",
    "IdentityDocumentKind",
    "LifecycleStatus",
    "ManifestKind",
    "PresentationKind",
    "ProtectedEnvelopeKind",
    "TokenKind",
    "VerificationOutcome",
]
