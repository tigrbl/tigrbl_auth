"""Standalone claim classes consumed by the RP ID-token profile."""

from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_authentication_context_concrete import AuthenticationContextClaim
from tigrbl_claim_authentication_methods_concrete import AuthenticationMethodsClaim
from tigrbl_claim_authentication_time_concrete import AuthenticationTimeClaim
from tigrbl_claim_authorized_party_concrete import AuthorizedPartyClaim
from tigrbl_claim_expiration_concrete import ExpirationClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_nonce_concrete import NonceClaim
from tigrbl_claim_subject_concrete import SubjectClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION

RP_ID_TOKEN_CLAIMS = (
    IssuerClaim,
    SubjectClaim,
    AudienceClaim,
    ExpirationClaim,
    IssuedAtClaim,
    AuthenticationTimeClaim,
    NonceClaim,
    AuthenticationContextClaim,
    AuthenticationMethodsClaim,
    AuthorizedPartyClaim,
)


def compose_rp_id_token_claim_set(*claims: object) -> ClaimSet:
    return ClaimSet(tuple(claims), "oidc-rp-id-token", CURRENT_VERSION.identifier)


__all__ = ["RP_ID_TOKEN_CLAIMS", "compose_rp_id_token_claim_set"]
