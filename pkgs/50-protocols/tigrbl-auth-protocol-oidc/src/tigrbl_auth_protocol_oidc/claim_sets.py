"""OIDC Core 1.0 claim-set composition."""

from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_authentication_context_claim_concrete import AuthenticationContextClaim
from tigrbl_authentication_methods_claim_concrete import AuthenticationMethodsClaim
from tigrbl_authentication_time_claim_concrete import AuthenticationTimeClaim
from tigrbl_authorized_party_claim_concrete import AuthorizedPartyClaim
from tigrbl_nonce_claim_concrete import NonceClaim
from tigrbl_transaction_id_claim_concrete import TransactionIdClaim
from tigrbl_verified_claims_claim_concrete import VerifiedClaimsClaim

OIDC_EXTENSION_CLAIMS = (
    AuthenticationTimeClaim,
    NonceClaim,
    AuthenticationContextClaim,
    AuthenticationMethodsClaim,
    AuthorizedPartyClaim,
    VerifiedClaimsClaim,
    TransactionIdClaim,
)


def compose_oidc_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "oidc", "1.0")


__all__ = ["OIDC_EXTENSION_CLAIMS", "compose_oidc_claim_set"]
