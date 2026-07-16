from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.resource_server import TokenValidationError
from tigrbl_security_trust_contracts import CapabilityMap
from tigrbl_token_introspection_bases import VerificationKeyCacheBase


class JWKSCache(VerificationKeyCacheBase):
    """In-memory `kid` to JWK cache for protected-resource verification."""

    def __init__(self) -> None:
        self._keys: dict[str, Mapping[str, Any]] = {}

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"key-resolution": ("jwks",)}, formats=("jwk", "jwks"))

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        return dict(self._keys)

    def put(self, key_id: str, key: Mapping[str, Any]) -> None:
        self._keys[str(key_id)] = dict(key)

    def put_many(self, keys: Mapping[str, Mapping[str, Any]]) -> None:
        for key_id, key in keys.items():
            self.put(key_id, key)

    def put_jwks(self, jwks: Mapping[str, Any]) -> None:
        for key in jwks.get("keys", []):
            kid = key.get("kid")
            if kid:
                self.put(str(kid), key)

    def get(self, key_id: str) -> Mapping[str, Any]:
        try:
            return self._keys[key_id]
        except KeyError as exc:
            raise TokenValidationError("unknown signing key") from exc


__all__ = ["JWKSCache"]
