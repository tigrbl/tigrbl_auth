from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_credential_status_claim_concrete import CredentialStatusClaim
from tigrbl_credential_type_claim_concrete import CredentialTypeClaim

SD_JWT_VC_CLAIM_CLASSES = (CredentialTypeClaim, CredentialStatusClaim)


def compose_sd_jwt_vc_claim_set(*claims) -> ClaimSet:
    if not any(isinstance(c, CredentialTypeClaim) for c in claims):
        raise ValueError("SD-JWT VC requires vct")
    return ClaimSet(tuple(claims), "sd-jwt-vc", "draft-ietf-oauth-sd-jwt-vc-17")


__all__ = ["SD_JWT_VC_CLAIM_CLASSES", "compose_sd_jwt_vc_claim_set"]
