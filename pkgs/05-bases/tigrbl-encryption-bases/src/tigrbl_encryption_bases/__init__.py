"""Reusable encryption and cipher-policy bases."""

from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from tigrbl_protected_artifact_bases import (
    ProtectedArtifactOpenerBase,
    RecipientSetEditorBase,
    SecurityArtifactIssuerBase,
)
from tigrbl_security_trust_contracts import (
    Artifact,
    DecryptRequest,
    EncryptRequest,
    ICapabilityProvider,
    ICipherPolicy,
    IEncryptionProvider,
    KeyRefLike,
    NormalizedDescriptor,
)


class EncryptionProviderBase(IEncryptionProvider, ICapabilityProvider, ABC):
    async def encrypt(self, request: EncryptRequest) -> Artifact:
        raise NotImplementedError

    async def decrypt(self, request: DecryptRequest) -> bytes:
        raise NotImplementedError


class CryptoDomainBase(
    ICapabilityProvider,
    SecurityArtifactIssuerBase,
    ProtectedArtifactOpenerBase,
    ABC,
):
    """Single-recipient artifact-encryption composition."""


class MreCryptoDomainBase(
    ICapabilityProvider,
    SecurityArtifactIssuerBase,
    ProtectedArtifactOpenerBase,
    RecipientSetEditorBase,
    ABC,
):
    """Multi-recipient artifact-encryption composition."""


class CipherPolicyDomainBase(ICipherPolicy, ICapabilityProvider, ABC):
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

    def lint(self) -> Sequence[str]:
        issues: list[str] = []
        for op, allowed in self.supports().ops.items():
            try:
                default = self.default_alg(op)
            except Exception as exc:  # pragma: no cover - defensive base behavior
                issues.append(f"default_alg({op}) raised: {exc!r}")
                continue
            if default not in set(allowed):
                issues.append(f"default_alg({op})={default} not in supports().ops[{op}]")
        return tuple(issues)


__all__ = [
    "CipherPolicyDomainBase",
    "CryptoDomainBase",
    "EncryptionProviderBase",
    "MreCryptoDomainBase",
]
