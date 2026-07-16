"""Versioned SD-JWT VC draft-profile ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .artifact import parse_sd_jwt_vc
from .claims import (
    SD_JWT_VC_CLAIM_CLASSES,
    SdJwtVcClaimSetPayload,
    compose_sd_jwt_vc_claim_set,
    parse_sd_jwt_vc_claims,
)
from .compatibility import (
    COMPATIBILITY_PATHS,
    SdJwtVcCompatibility,
    compatibility,
)
from .errors import (
    SdJwtVcKeyBindingError,
    SdJwtVcProfileError,
    UnsupportedSdJwtVcMediaTypeError,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .metadata import SdJwtVcTypeMetadata, parse_type_metadata
from .schemas import (
    LEGACY_SD_JWT_VC_TYP,
    SD_JWT_VC_CARRIER,
    SdJwtVcCarrier,
    select_carrier,
)
from .versions import CURRENT_VERSION, VERSION_HISTORY, SdJwtVcVersion, select_version
from .status import SdJwtVcStatusReference, parse_status_reference
from .validation import validate_sd_jwt_vc
from tigrbl_sd_jwt_vc_credential_concrete import SdJwtVcCredential

DRAFT_REVISION = "draft-ietf-oauth-sd-jwt-vc-17"
MEDIA_TYPE = SD_JWT_VC_CARRIER.media_type
TYP = SD_JWT_VC_CARRIER.typ
SdJwtVc = SdJwtVcCredential


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="sd-jwt-vc",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_eat_sd_jwt_vc_profiles.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "DRAFT_REVISION",
    "FEATURES_BY_VERSION",
    "LEGACY_SD_JWT_VC_TYP",
    "MEDIA_TYPE",
    "SD_JWT_VC_CARRIER",
    "SD_JWT_VC_CLAIM_CLASSES",
    "SdJwtVcClaimSetPayload",
    "SdJwtVcCredential",
    "SdJwtVcStatusReference",
    "SdJwtVcTypeMetadata",
    "VERSION_HISTORY",
    "SdJwtVcCarrier",
    "SdJwtVc",
    "SdJwtVcCompatibility",
    "SdJwtVcKeyBindingError",
    "SdJwtVcProfileError",
    "SdJwtVcVersion",
    "TYP",
    "UnsupportedSdJwtVcMediaTypeError",
    "capability_report",
    "compatibility",
    "compose_sd_jwt_vc_claim_set",
    "migrate_claims",
    "parse_sd_jwt_vc",
    "parse_sd_jwt_vc_claims",
    "parse_status_reference",
    "parse_type_metadata",
    "select_carrier",
    "select_version",
    "supports",
    "validate_sd_jwt_vc",
]
