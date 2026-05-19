"""JWKS publication helpers for the release path."""

from __future__ import annotations


async def build_jwks_document() -> dict:
    from tigrbl_auth.standards.oidc.id_token import ensure_rsa_jwt_key, rsa_key_provider, rotation_jwks_cache
    from tigrbl_auth.services.key_management import _ensure_key as ensure_ed25519_key, _provider as ed25519_provider

    await ensure_rsa_jwt_key()
    await ensure_ed25519_key()
    rsa = await rsa_key_provider().jwks()
    ed = await ed25519_provider().jwks()
    combined = {k.get("kid"): k for k in [*rotation_jwks_cache(), *rsa.get("keys", []), *ed.get("keys", [])]}
    return {"keys": list(combined.values())}


__all__ = ["build_jwks_document"]
