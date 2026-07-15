"""OAuth extension claim composition from standalone claim packages."""

from tigrbl_claim_access_token_digest_concrete import AccessTokenDigestClaim
from tigrbl_claim_actor_concrete import ActorClaim
from tigrbl_claim_client_id_concrete import ClientIdClaim
from tigrbl_claim_confirmation_concrete import ConfirmationClaim
from tigrbl_claim_http_method_concrete import HttpMethodClaim
from tigrbl_claim_http_uri_concrete import HttpUriClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_claim_may_act_concrete import MayActClaim
from tigrbl_claim_nonce_concrete import NonceClaim
from tigrbl_claim_scope_concrete import ScopeClaim
from tigrbl_identity_contracts.claims import ClaimSet

OAUTH_EXTENSION_CLAIMS = (ClientIdClaim, ScopeClaim, ConfirmationClaim)
OAUTH_DPOP_PROOF_CLAIMS = (
    JwtIdClaim,
    HttpMethodClaim,
    HttpUriClaim,
    IssuedAtClaim,
    NonceClaim,
    AccessTokenDigestClaim,
)
OAUTH_TOKEN_EXCHANGE_CLAIMS = (ActorClaim, MayActClaim)


def _compose(
    claims: tuple[object, ...],
    *,
    allowed: tuple[type, ...],
    protocol: str,
    version: str,
) -> ClaimSet:
    unexpected = [
        getattr(claim, "name", type(claim).__name__)
        for claim in claims
        if not isinstance(claim, allowed)
    ]
    if unexpected:
        raise ValueError(f"claims are not valid for {protocol}: {unexpected}")
    return ClaimSet(claims, protocol, version)


def compose_oauth_claim_set(*claims: object) -> ClaimSet:
    return _compose(
        claims,
        allowed=OAUTH_EXTENSION_CLAIMS,
        protocol="oauth-jwt-access-token",
        version="RFC 9068",
    )


def compose_dpop_proof_claim_set(*claims: object) -> ClaimSet:
    return _compose(
        claims,
        allowed=OAUTH_DPOP_PROOF_CLAIMS,
        protocol="dpop-proof",
        version="RFC9449",
    )


def compose_token_exchange_claim_set(*claims: object) -> ClaimSet:
    return _compose(
        claims,
        allowed=OAUTH_TOKEN_EXCHANGE_CLAIMS,
        protocol="oauth-token-exchange",
        version="RFC8693",
    )


__all__ = [
    "OAUTH_DPOP_PROOF_CLAIMS",
    "OAUTH_EXTENSION_CLAIMS",
    "OAUTH_TOKEN_EXCHANGE_CLAIMS",
    "compose_dpop_proof_claim_set",
    "compose_oauth_claim_set",
    "compose_token_exchange_claim_set",
]
