"""RFC 9711 claim-family composition."""

from tigrbl_claim_eat_nonce_concrete import EatNonceClaim
from tigrbl_claim_eat_profile_concrete import EatProfileClaim
from tigrbl_claim_eat_submodules_concrete import EatSubmodulesClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_ueid_concrete import UeidClaim
from tigrbl_identity_contracts.claims import ClaimSet

EAT_CLAIM_CLASSES = (
    EatProfileClaim,
    EatNonceClaim,
    IssuedAtClaim,
    UeidClaim,
    EatSubmodulesClaim,
)


def compose_eat_claim_set(*claims: object) -> ClaimSet:
    return ClaimSet(tuple(claims), "eat", "RFC9711")


__all__ = ["EAT_CLAIM_CLASSES", "compose_eat_claim_set"]
