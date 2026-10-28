"""OAuth extension claim composition from standalone claim packages."""

from tba_concrete_claim_access_token_digest import AccessTokenDigestClaim
from tba_concrete_claim_actor import ActorClaim
from tba_concrete_claim_client_id import ClientIdClaim
from tba_concrete_claim_confirmation import ConfirmationClaim
from tba_concrete_claim_http_method import HttpMethodClaim
from tba_concrete_claim_http_uri import HttpUriClaim
from tba_concrete_claim_issued_at import IssuedAtClaim
from tba_concrete_claim_jwt_id import JwtIdClaim
from tba_concrete_claim_may_act import MayActClaim
from tba_concrete_claim_nonce import NonceClaim
from tba_concrete_claim_scope import ScopeClaim
from tba_contracts_identity.claims import ClaimSet

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
