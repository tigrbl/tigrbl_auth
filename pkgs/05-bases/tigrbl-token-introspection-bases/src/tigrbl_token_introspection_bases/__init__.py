"""Reusable token-introspection and key-cache bases."""

from abc import ABC
from typing import Any, Mapping

from tigrbl_security_trust_contracts import (
    ICapabilityProvider,
    ITokenIntrospectionClient,
    IVerificationKeyCache,
    IVerificationKeyResolver,
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
)


class VerificationKeyResolverBase(IVerificationKeyResolver, ICapabilityProvider, ABC):
    def get(self, key_id: str) -> Mapping[str, Any]:
        raise NotImplementedError


class VerificationKeyCacheBase(IVerificationKeyCache, VerificationKeyResolverBase):
    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        raise NotImplementedError

    def put(self, key_id: str, key: Mapping[str, Any]) -> None:
        raise NotImplementedError

    def put_many(self, keys: Mapping[str, Mapping[str, Any]]) -> None:
        for key_id, key in keys.items():
            self.put(key_id, key)


class TokenIntrospectionClientBase(ITokenIntrospectionClient, ICapabilityProvider, ABC):
    def introspect(self, request: TokenIntrospectionRequest) -> TokenIntrospectionResult:
        raise NotImplementedError


__all__ = [
    "TokenIntrospectionClientBase",
    "VerificationKeyCacheBase",
    "VerificationKeyResolverBase",
]
