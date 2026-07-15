"""Versioned SD-JWT VC draft-profile ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import SD_JWT_VC_CLAIM_CLASSES, compose_sd_jwt_vc_claim_set
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
from .schemas import (
    LEGACY_SD_JWT_VC_TYP,
    SD_JWT_VC_CARRIER,
    SdJwtVcCarrier,
    select_carrier,
)
from .versions import CURRENT_VERSION, VERSION_HISTORY, SdJwtVcVersion, select_version


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
    "FEATURES_BY_VERSION",
    "LEGACY_SD_JWT_VC_TYP",
    "SD_JWT_VC_CARRIER",
    "SD_JWT_VC_CLAIM_CLASSES",
    "VERSION_HISTORY",
    "SdJwtVcCarrier",
    "SdJwtVcCompatibility",
    "SdJwtVcKeyBindingError",
    "SdJwtVcProfileError",
    "SdJwtVcVersion",
    "UnsupportedSdJwtVcMediaTypeError",
    "capability_report",
    "compatibility",
    "compose_sd_jwt_vc_claim_set",
    "migrate_claims",
    "select_carrier",
    "select_version",
    "supports",
]
