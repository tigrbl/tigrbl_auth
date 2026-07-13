'Key lifecycle, crypto, binding, and resolver bases.'
from __future__ import annotations

from .bases import *  # noqa: F401,F403

class KeyLifecycleProviderBase(IKeyLifecycleProvider, CapabilityProviderBase):
    """Base for provider-neutral key creation, import, rotation, and destruction."""

    async def create_key(self, spec: KeySpec) -> KeyHandle:
        raise NotImplementedError

    async def import_key(
        self,
        spec: KeySpec,
        material: bytes,
        *,
        public: bytes | None = None,
    ) -> KeyHandle:
        raise NotImplementedError

    async def rotate_key(
        self,
        kid: str,
        *,
        spec_overrides: Mapping[str, Any] | None = None,
    ) -> KeyHandle:
        raise NotImplementedError

    async def destroy_key(self, kid: str, version: int | None = None) -> bool:
        raise NotImplementedError


class KeyResolverBase(IKeyResolver, CapabilityProviderBase):
    """Base for resolving opaque key references into provider handles."""

    async def resolve_key(
        self,
        ref: KeyRefLike,
        *,
        include_secret: bool = False,
    ) -> KeyRefLike:
        raise NotImplementedError


class EncryptionProviderBase(IEncryptionProvider, CapabilityProviderBase):
    """Base for data encryption and decryption providers."""

    async def encrypt(self, request: EncryptRequest) -> Artifact:
        raise NotImplementedError

    async def decrypt(self, request: DecryptRequest) -> bytes:
        raise NotImplementedError


class KeyWrappingProviderBase(IKeyWrappingProvider, CapabilityProviderBase):
    """Base for key wrapping and unwrapping providers."""

    async def wrap_key(self, request: WrapKeyRequest) -> WrappedKeyMaterial:
        raise NotImplementedError

    async def unwrap_key(self, request: UnwrapKeyRequest) -> KeyMaterial:
        raise NotImplementedError


class KeyEncapsulationProviderBase(IKeyEncapsulationProvider, CapabilityProviderBase):
    """Base for KEM encapsulation and decapsulation providers."""

    async def encapsulate(self, request: EncapsulateRequest) -> EncapsulationResult:
        raise NotImplementedError

    async def decapsulate(self, request: DecapsulateRequest) -> bytes:
        raise NotImplementedError


class AttestationProviderBase(IAttestationProvider, CapabilityProviderBase):
    """Base for key attestation and evidence verification providers."""

    async def attest_key(self, request: AttestKeyRequest) -> AttestationEvidence:
        raise NotImplementedError

    async def verify_attestation(
        self,
        request: VerifyAttestationRequest,
    ) -> VerificationResult:
        raise NotImplementedError


class PublicKeyExporterBase(IPublicKeyExporter, CapabilityProviderBase):
    """Base for public key material export."""

    async def export_public_key(
        self,
        request: ExportPublicKeyRequest,
    ) -> ExportPublicKeyResult:
        raise NotImplementedError


class CryptoKeyProviderBase(
    KeyLifecycleProviderBase,
    KeyResolverBase,
    SigningProviderBase,
    EncryptionProviderBase,
    KeyWrappingProviderBase,
    KeyEncapsulationProviderBase,
    AttestationProviderBase,
    PublicKeyExporterBase,
):
    """Composite base for providers that intentionally implement the full key surface."""


class CipherPolicyDomainBase(ICipherPolicy, CapabilityProviderBase):
    """Domain base for cipher-suite policy, defaults, dialect mapping, and linting."""

    @abstractmethod
    def suite_id(self) -> str: ...

    @abstractmethod
    def default_alg(self, op: str, *, for_key: KeyRefLike | None = None) -> str: ...

    @abstractmethod
    def normalize(
        self,
        *,
        op: str,
        alg: str | None = None,
        key: KeyRefLike | None = None,
        params: Mapping[str, Any] | None = None,
        dialect: str | None = None,
    ) -> NormalizedDescriptor: ...

    def policy(self) -> Mapping[str, Any]:
        raise NotImplementedError

    def features(self) -> Mapping[str, Any]:
        raise NotImplementedError

    def lint(self) -> Sequence[str]:
        return self._lint()

    def _lint(self) -> Sequence[str]:
        issues: list[str] = []
        supported = self.supports().ops
        for op, allowed in supported.items():
            try:
                default = self.default_alg(op)
            except Exception as exc:  # pragma: no cover - defensive base behavior
                issues.append(f"default_alg({op}) raised: {exc!r}")
                continue
            if default not in set(allowed):
                issues.append(
                    f"default_alg({op})={default} not in supports().ops[{op}]"
                )
        return tuple(issues)


class ConfirmationBindingValidatorBase(
    IConfirmationBindingValidator, CapabilityProviderBase
):
    """Base for proof confirmation validators such as DPoP or mTLS cnf checks."""

    @property
    @abstractmethod
    def confirmation_member(self) -> str: ...

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: ProofBinding | None,
    ) -> bool:
        raise NotImplementedError


class SenderConstraintValidatorBase(ISenderConstraintValidator, CapabilityProviderBase):
    """Base for composing sender-constraint validation providers."""

    def validate(
        self,
        cnf: Mapping[str, Any],
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
        require_dpop: bool = False,
        require_mtls: bool = False,
    ) -> bool:
        raise NotImplementedError


class VerificationKeyResolverBase(IVerificationKeyResolver, CapabilityProviderBase):
    """Base for verification key resolution."""

    def get(self, key_id: str) -> Mapping[str, Any]:
        raise NotImplementedError


class VerificationKeyCacheBase(IVerificationKeyCache, VerificationKeyResolverBase):
    """Base for mutable verification-key caches independent of source format."""

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        raise NotImplementedError

    def put(self, key_id: str, key: Mapping[str, Any]) -> None:
        raise NotImplementedError

    def put_many(self, keys: Mapping[str, Mapping[str, Any]]) -> None:
        for key_id, key in keys.items():
            self.put(key_id, key)


class TokenIntrospectionClientBase(ITokenIntrospectionClient, CapabilityProviderBase):
    """Base for provider-neutral token introspection clients."""

    def introspect(
        self,
        request: TokenIntrospectionRequest,
    ) -> TokenIntrospectionResult:
        raise NotImplementedError
