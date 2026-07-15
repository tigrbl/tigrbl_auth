"""SD-JWT VC claim-set composition."""

from tigrbl_claim_credential_status_concrete import CredentialStatusClaim
from tigrbl_claim_credential_type_concrete import CredentialTypeClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION

SD_JWT_VC_CLAIM_CLASSES = (CredentialTypeClaim, CredentialStatusClaim)


def compose_sd_jwt_vc_claim_set(*claims: object) -> ClaimSet:
    if not any(isinstance(claim, CredentialTypeClaim) for claim in claims):
        raise ValueError("SD-JWT VC requires vct")
    return ClaimSet(tuple(claims), "sd-jwt-vc", CURRENT_VERSION.identifier)


__all__ = ["SD_JWT_VC_CLAIM_CLASSES", "compose_sd_jwt_vc_claim_set"]
