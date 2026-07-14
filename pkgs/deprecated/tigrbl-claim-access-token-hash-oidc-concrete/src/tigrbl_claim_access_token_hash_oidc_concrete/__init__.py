"""Deprecated compatibility facade for the standalone ``at_hash`` claim."""

import warnings

from tigrbl_claim_access_token_hash_concrete import AccessTokenHashClaim

warnings.warn(
    "tigrbl_claim_access_token_hash_oidc_concrete is deprecated; import "
    "AccessTokenHashClaim from tigrbl_claim_access_token_hash_concrete",
    DeprecationWarning,
    stacklevel=2,
)

OidcAccessTokenHashClaim = AccessTokenHashClaim

__all__ = ["AccessTokenHashClaim", "OidcAccessTokenHashClaim"]
