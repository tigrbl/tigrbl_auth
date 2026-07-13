from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_claim_credential_status_concrete import CredentialStatusClaim
from tigrbl_claim_credential_type_concrete import CredentialTypeClaim

from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .versions import CURRENT_VERSION, VERSION_HISTORY, SdJwtVcVersion, select_version

SD_JWT_VC_CLAIM_CLASSES = (CredentialTypeClaim, CredentialStatusClaim)


def compose_sd_jwt_vc_claim_set(*claims) -> ClaimSet:
    if not any(isinstance(c, CredentialTypeClaim) for c in claims):
        raise ValueError("SD-JWT VC requires vct")
    return ClaimSet(tuple(claims), "sd-jwt-vc", "draft-17")


__all__ = [
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "SD_JWT_VC_CLAIM_CLASSES",
    "VERSION_HISTORY",
    "SdJwtVcVersion",
    "compose_sd_jwt_vc_claim_set",
    "migrate_claims",
    "select_version",
    "supports",
]
