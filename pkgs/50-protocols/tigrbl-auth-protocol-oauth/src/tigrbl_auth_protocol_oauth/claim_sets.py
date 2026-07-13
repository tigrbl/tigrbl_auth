"""OAuth JWT access-token claim-set composition."""

from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_claim_client_id_concrete import ClientIdClaim
from tigrbl_claim_confirmation_concrete import ConfirmationClaim
from tigrbl_claim_scope_concrete import ScopeClaim
from tigrbl_claim_access_token_hash_concrete import AccessTokenHashClaim
from tigrbl_claim_actor_concrete import ActorClaim
from tigrbl_claim_http_method_concrete import HttpMethodClaim
from tigrbl_claim_http_uri_concrete import HttpUriClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_claim_may_act_concrete import MayActClaim
from tigrbl_claim_nonce_concrete import NonceClaim

OAUTH_EXTENSION_CLAIMS = (ClientIdClaim, ScopeClaim, ConfirmationClaim)
OAUTH_DPOP_PROOF_CLAIMS = (
    JwtIdClaim,
    HttpMethodClaim,
    HttpUriClaim,
    IssuedAtClaim,
    NonceClaim,
    AccessTokenHashClaim,
)
OAUTH_TOKEN_EXCHANGE_CLAIMS = (ActorClaim, MayActClaim)


def compose_oauth_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "oauth-jwt-access-token", "RFC 9068")


def compose_dpop_proof_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "dpop-proof", "RFC9449")


def compose_token_exchange_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "oauth-token-exchange", "RFC8693")


__all__ = [
    "OAUTH_DPOP_PROOF_CLAIMS",
    "OAUTH_EXTENSION_CLAIMS",
    "OAUTH_TOKEN_EXCHANGE_CLAIMS",
    "compose_dpop_proof_claim_set",
    "compose_oauth_claim_set",
    "compose_token_exchange_claim_set",
]
