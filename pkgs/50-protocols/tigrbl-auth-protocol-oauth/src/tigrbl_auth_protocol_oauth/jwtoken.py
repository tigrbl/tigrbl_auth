"""Compatibility export for the environment-backed JOSE provider.

OAuth wire/profile modules may consume the provider, but key loading, key
creation, filesystem access, and token service construction remain in layer 20.
"""

from tigrbl_identity_jose.jwt_coder import JWTCoder
from tigrbl_identity_jose.errors import InvalidTokenError
from tigrbl_identity_contracts.tokens import (
    DEFAULT_ACCESS_TOKEN_TTL as _ACCESS_TTL,
    DEFAULT_REFRESH_TOKEN_TTL as _REFRESH_TTL,
)

_ALG = "EdDSA"

__all__ = ["InvalidTokenError", "JWTCoder", "_ACCESS_TTL", "_ALG", "_REFRESH_TTL"]
