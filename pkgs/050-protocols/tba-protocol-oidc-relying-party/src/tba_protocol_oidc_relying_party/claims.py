"""Standalone claim classes consumed by the RP ID-token profile."""

from tba_concrete_claim_audience import AudienceClaim
from tba_concrete_claim_authentication_context import AuthenticationContextClaim
from tba_concrete_claim_authentication_methods import AuthenticationMethodsClaim
from tba_concrete_claim_authentication_time import AuthenticationTimeClaim
from tba_concrete_claim_authorized_party import AuthorizedPartyClaim
from tba_concrete_claim_expiration import ExpirationClaim
from tba_concrete_claim_issued_at import IssuedAtClaim
from tba_concrete_claim_issuer import IssuerClaim
from tba_concrete_claim_nonce import NonceClaim
from tba_concrete_claim_subject import SubjectClaim
from tba_contracts_identity.claims import ClaimSet

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
