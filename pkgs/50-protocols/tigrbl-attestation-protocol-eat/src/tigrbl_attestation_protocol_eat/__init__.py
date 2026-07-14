from .bindings import CAPABILITY_REQUIREMENTS
from .claims import EAT_CLAIM_CLASSES, compose_eat_claim_set
from .compatibility import COMPATIBILITY_PATHS, EatCompatibility, compatibility
from .errors import EatProfileBindingError, EatProtocolError, UnsupportedEatCarrierError
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .schemas import (
    EAT_CARRIERS,
    EAT_CWT_CARRIER,
    EAT_JWT_CARRIER,
    EatCarrier,
    select_carrier,
)
from .versions import CURRENT_VERSION, VERSION_HISTORY, EatVersion, select_version
from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report as _build_protocol_capability_report,
)


def capability_report() -> dict[str, object]:
    return _build_protocol_capability_report(
        protocol="eat",
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
    "EAT_CARRIERS",
    "EAT_CLAIM_CLASSES",
    "EAT_CWT_CARRIER",
    "EAT_JWT_CARRIER",
    "FEATURES_BY_VERSION",
    "VERSION_HISTORY",
    "EatCarrier",
    "EatCompatibility",
    "EatProfileBindingError",
    "EatProtocolError",
    "EatVersion",
    "UnsupportedEatCarrierError",
    "capability_report",
    "compatibility",
    "compose_eat_claim_set",
    "migrate_claims",
    "select_carrier",
    "select_version",
    "supports",
]
