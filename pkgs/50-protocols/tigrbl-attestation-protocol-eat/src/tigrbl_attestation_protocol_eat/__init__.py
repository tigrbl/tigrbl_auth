from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_claim_eat_profile_concrete import EatProfileClaim
from tigrbl_claim_eat_nonce_concrete import EatNonceClaim
from tigrbl_claim_eat_submodules_concrete import EatSubmodulesClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_ueid_concrete import UeidClaim

from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .versions import CURRENT_VERSION, VERSION_HISTORY, EatVersion, select_version

EAT_CLAIM_CLASSES = (
    EatProfileClaim,
    EatNonceClaim,
    IssuedAtClaim,
    UeidClaim,
    EatSubmodulesClaim,
)


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
