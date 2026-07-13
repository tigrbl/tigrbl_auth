'Key request, result, and lifecycle value objects.'
from __future__ import annotations

from .keys import *  # noqa: F401,F403

class KeyStatus(str, Enum):
    """Durable key lifecycle status."""

    ACTIVE = "active"
    DISABLED = "disabled"
    RETIRED = "retired"
    DESTROYED = "destroyed"


class KeyOrigin(str, Enum):
    """Where key material originated."""

    GENERATED = "generated"
    IMPORTED = "imported"
    DERIVED = "derived"
    EXTERNAL = "external"


class KeyExportPolicy(str, Enum):
    """Material export policy."""

    PUBLIC_ONLY = "public_only"
    WRAPPED_ONLY = "wrapped_only"
    NON_EXTRACTABLE = "non_extractable"
    PROVIDER_CONTROLLED = "provider_controlled"


class KeyMaterialFormat(str, Enum):
    """Portable public or wrapped key material formats."""

    RAW_PUBLIC = "raw-public"
    JWK = "jwk"
    JWKS = "jwks"
    PEM = "pem"
    DER = "der"
    COSE_KEY = "cose-key"
    SSH_PUBLIC = "ssh-public"
    WRAPPED = "wrapped"
    PROVIDER_REF = "provider-ref"


@dataclass(frozen=True)
class KeySpec:
    """Provider-neutral key creation/import specification."""

    kid: str | None = None
    kind: KeyKind | str = KeyKind.ASYMMETRIC
    usages: Sequence[KeyUsage | str] = ()
    allowed_ops: Sequence[KeyOperation | str] = ()
    alg: Alg | None = None
    extractable: bool = False
    export_policy: KeyExportPolicy | str = KeyExportPolicy.PUBLIC_ONLY
    origin: KeyOrigin | str = KeyOrigin.GENERATED
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KeyHandle:
    """Opaque provider key handle plus public description."""

    ref: KeyRefLike
    kid: str | None = None
    version: int | None = None
    alg: Alg | None = None
    kind: KeyKind | str | None = None
    provider: str | None = None
    public_material: bytes | Mapping[str, Any] | str | None = None
    public_material_format: KeyMaterialFormat | str | None = None
    fingerprint: str | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KeyVersionDescriptor:
    """Provider-neutral key version descriptor."""

    kid: str
    version: int
    status: KeyStatus | str = KeyStatus.ACTIVE
    alg: Alg | None = None
    allowed_ops: Sequence[KeyOperation | str] = ()
    public_material: bytes | Mapping[str, Any] | str | None = None
    public_material_format: KeyMaterialFormat | str | None = None
    fingerprint: str | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SignRequest:
    """Input to a signing provider."""

    payload: bytes | str
    key: KeyRefLike
    alg: Alg | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SignResult:
    """Signature result."""

    signature: bytes | str
    alg: Alg | None = None
    format: ArtifactFormat = "raw-signature"
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VerifySignatureRequest:
    """Input to a signature verifier."""

    payload: bytes | str
    signature: bytes | str | Artifact
    key: KeyRefLike
    alg: Alg | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VerifySignatureResult:
    """Signature verification result."""

    valid: bool
    reason: str | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EncryptRequest:
    """Input to a data encryption provider."""

    plaintext: bytes
    key: KeyRefLike
    alg: Alg | None = None
    aad: bytes | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DecryptRequest:
    """Input to a data decryption provider."""

    ciphertext: bytes | Artifact
    key: KeyRefLike
    alg: Alg | None = None
    aad: bytes | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WrapKeyRequest:
    """Input to wrapping key material with a KEK."""

    material: bytes | KeyRefLike
    wrapping_key: KeyRefLike
    alg: Alg | None = None
    aad: bytes | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UnwrapKeyRequest:
    """Input to unwrapping key material with a KEK."""

    wrapped: bytes | Artifact
    wrapping_key: KeyRefLike
    alg: Alg | None = None
    aad: bytes | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WrappedKeyMaterial:
    """Wrapped key material and envelope metadata."""

    wrapped: bytes | str
    alg: Alg | None = None
    wrapping_key_ref: KeyRefLike | None = None
    material_format: KeyMaterialFormat | str = KeyMaterialFormat.WRAPPED
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EncapsulateRequest:
    """Input to KEM encapsulation."""

    public_key: KeyRefLike
    alg: Alg | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DecapsulateRequest:
    """Input to KEM decapsulation."""

    ciphertext: bytes | str
    secret_key: KeyRefLike
    alg: Alg | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EncapsulationResult:
    """KEM ciphertext and derived shared secret."""

    ciphertext: bytes | str
    shared_secret: bytes
    alg: Alg | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AttestKeyRequest:
    """Input to key attestation."""

    key: KeyRefLike
    claims: Mapping[str, Any] = field(default_factory=dict)
    alg: Alg | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VerifyAttestationRequest:
    """Input to key attestation verification."""

    evidence: Artifact | Mapping[str, Any] | bytes | str
    trust_roots: Sequence[KeyRefLike] = ()
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AttestationEvidence:
    """Portable key attestation evidence envelope."""

    evidence: Artifact | Mapping[str, Any] | bytes | str
    format: ArtifactFormat
    subject_key_ref: KeyRefLike | None = None
    issuer_key_ref: KeyRefLike | None = None
    claims: Mapping[str, Any] = field(default_factory=dict)
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExportPublicKeyRequest:
    """Input to public key export."""

    key: KeyRefLike
    format: KeyMaterialFormat | str = KeyMaterialFormat.JWK
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExportPublicKeyResult:
    """Public key material in the requested format."""

    material: bytes | Mapping[str, Any] | str
    format: KeyMaterialFormat | str
    fingerprint: str | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


__all__ = [
    "AttestKeyRequest",
    "AttestationEvidence",
    "DecapsulateRequest",
    "DecryptRequest",
    "EncapsulateRequest",
    "EncapsulationResult",
    "EncryptRequest",
    "ExportPublicKeyRequest",
    "ExportPublicKeyResult",
    "KEY_USAGE_SPECS",
    "KeyExportPolicy",
    "KeyHandle",
    "KeyKind",
    "KeyMaterialFormat",
    "KeyOperation",
    "KeyOrigin",
    "KeySpec",
    "KeyStatus",
    "KeyUsage",
    "KeyUsageSpec",
    "KeyVersionDescriptor",
    "SignRequest",
    "SignResult",
    "UnwrapKeyRequest",
    "VerifyAttestationRequest",
    "VerifySignatureRequest",
    "VerifySignatureResult",
    "WrappedKeyMaterial",
    "WrapKeyRequest",
    "coerce_key_kind",
    "coerce_key_operation",
    "coerce_key_usage",
    "default_key_operations",
    "key_usage_spec",
    "maximum_key_operations",
    "normalize_key_operations",
    "normalize_key_usages",
    "resolve_key_allowed_operations",
]
