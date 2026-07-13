"""Compatibility export for OIDC ID Token protocol helpers."""

from tigrbl_identity_jose.oidc_key_runtime import _RSA_KEY_PATH, rsa_key_provider as _provider

_service_cache = None
from .standards.id_token import (
    ensure_rsa_jwt_key,
    mint_id_token,
    oidc_hash,
    rsa_key_provider,
    rotate_rsa_jwt_key,
    rotation_jwks_cache,
    verify_id_token,
)

__all__ = [
    "ensure_rsa_jwt_key", "mint_id_token", "oidc_hash", "rsa_key_provider",
    "rotate_rsa_jwt_key", "rotation_jwks_cache", "verify_id_token",
]
