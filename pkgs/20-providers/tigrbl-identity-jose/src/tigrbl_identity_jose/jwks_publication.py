"""Combined public JWKS publication for Tigrbl Auth-owned keys."""
from .key_management import _ensure_key as ensure_ed25519_key, _provider as ed25519_provider
from .oidc_key_runtime import ensure_rsa_jwt_key, rsa_key_provider, rotation_jwks_cache

async def build_combined_jwks_document() -> dict[str, object]:
    await ensure_rsa_jwt_key(); await ensure_ed25519_key()
    rsa = await rsa_key_provider().jwks(); ed = await ed25519_provider().jwks()
    combined = {key.get("kid"): key for key in [*rotation_jwks_cache(), *rsa.get("keys", []), *ed.get("keys", [])] if key.get("kid")}
    return {"keys": list(combined.values())}

__all__ = ["build_combined_jwks_document"]
