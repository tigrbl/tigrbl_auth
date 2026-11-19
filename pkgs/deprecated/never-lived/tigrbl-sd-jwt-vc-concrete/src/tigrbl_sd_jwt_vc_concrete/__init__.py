"""Compatibility facade for the canonical SD-JWT VC object and profile owner."""

from tigrbl_credential_profile_sd_jwt_vc import *  # noqa: F403
from tigrbl_credential_profile_sd_jwt_vc import __all__ as _profile_exports
from tigrbl_sd_jwt_vc_credential_concrete import SdJwtVcCredential

SdJwtVc = SdJwtVcCredential
DRAFT_REVISION = "draft-ietf-oauth-sd-jwt-vc-17"
MEDIA_TYPE = "application/dc+sd-jwt"
TYP = "dc+sd-jwt"
__all__ = [*_profile_exports, "DRAFT_REVISION", "MEDIA_TYPE", "SdJwtVc", "TYP"]
