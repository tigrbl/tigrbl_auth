"""OAuth JWT access-token claim-set composition."""

from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_claim_client_id_concrete import ClientIdClaim
from tigrbl_claim_confirmation_concrete import ConfirmationClaim
from tigrbl_claim_scope_concrete import ScopeClaim

OAUTH_EXTENSION_CLAIMS = (ClientIdClaim, ScopeClaim, ConfirmationClaim)


def compose_oauth_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "oauth-jwt-access-token", "RFC 9068")


__all__ = ["OAUTH_EXTENSION_CLAIMS", "compose_oauth_claim_set"]
