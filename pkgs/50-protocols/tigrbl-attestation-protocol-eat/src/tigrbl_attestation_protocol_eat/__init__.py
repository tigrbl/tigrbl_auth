from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_eat_profile_claim_concrete import EatProfileClaim
from tigrbl_nonce_claim_concrete import NonceClaim

from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .versions import CURRENT_VERSION, VERSION_HISTORY, EatVersion, select_version

EAT_CLAIM_CLASSES = (EatProfileClaim, NonceClaim)


def compose_eat_claim_set(*claims) -> ClaimSet:
    return ClaimSet(tuple(claims), "eat", "RFC9711")


__all__ = [
    "CURRENT_VERSION",
    "EAT_CLAIM_CLASSES",
    "FEATURES_BY_VERSION",
    "VERSION_HISTORY",
    "EatVersion",
    "compose_eat_claim_set",
    "migrate_claims",
    "select_version",
    "supports",
]
