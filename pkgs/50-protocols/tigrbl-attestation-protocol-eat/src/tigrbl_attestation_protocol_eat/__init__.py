from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_eat_profile_claim_concrete import EatProfileClaim
from tigrbl_nonce_claim_concrete import NonceClaim

EAT_CLAIM_CLASSES = (EatProfileClaim, NonceClaim)


def compose_eat_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "eat", "RFC 9711")


__all__ = ["EAT_CLAIM_CLASSES", "compose_eat_claim_set"]
