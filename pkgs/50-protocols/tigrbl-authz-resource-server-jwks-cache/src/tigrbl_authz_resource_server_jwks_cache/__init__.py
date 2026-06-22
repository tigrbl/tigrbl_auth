from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.resource_server import TokenValidationError


class JWKSCache:
    """In-memory `kid` to JWK cache for protected-resource verification."""

    def __init__(self) -> None:
        self._keys: dict[str, Mapping[str, Any]] = {}

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        return dict(self._keys)

    def put_jwks(self, jwks: Mapping[str, Any]) -> None:
        for key in jwks.get("keys", []):
            kid = key.get("kid")
            if kid:
                self._keys[str(kid)] = dict(key)

    def get(self, kid: str) -> Mapping[str, Any]:
        try:
            return self._keys[kid]
        except KeyError as exc:
            raise TokenValidationError("unknown signing key") from exc


__all__ = ["JWKSCache"]
