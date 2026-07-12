"""Dependency-light taxonomy for identity and security artifacts."""

from enum import Enum


class ArtifactKind(str, Enum):
    CREDENTIAL = "credential"
    TOKEN = "token"
    PRESENTATION = "presentation"
    ATTESTATION = "attestation"
    MANIFEST = "manifest"
    CERTIFICATE = "certificate"
    STATUS = "status"


class CredentialFormat(str, Enum):
    W3C_VCDM = "w3c-vcdm"
    SD_JWT_VC = "sd-jwt-vc"
    ISO_MDOC = "iso-mdoc"
    X509 = "x509"
    X509_SVID = "x509-svid"
    JWT_SVID = "jwt-svid"


class TokenKind(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    ID = "id"
    SECURITY_EVENT = "security-event"
    ENTITY_ATTESTATION = "entity-attestation"
    WORKLOAD_IDENTITY = "workload-identity"
    PROOF = "proof"
    CONTINUATION = "continuation"


class PresentationKind(str, Enum):
    W3C_VP = "w3c-vp"
    SD_JWT = "sd-jwt"
    ISO_MDOC = "iso-mdoc"


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
    "LifecycleStatus",
    "ManifestKind",
    "PresentationKind",
    "TokenKind",
    "VerificationOutcome",
]
