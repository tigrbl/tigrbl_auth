"""Versioned RFC 8417 Security Event Token ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import SET_CLAIM_CLASSES, compose_set_claim_set
from .compatibility import COMPATIBILITY_PATHS, SetCompatibility, compatibility
from .errors import SetProtocolError, SetUsageError, UnsupportedSetMediaTypeError
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .schemas import SET_JWT_CARRIER, SetCarrier, select_carrier
from .versions import CURRENT_VERSION, VERSION_HISTORY, SetVersion, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="set",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_set_protocol.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "SET_CLAIM_CLASSES",
    "SET_JWT_CARRIER",
    "VERSION_HISTORY",
    "SetCarrier",
    "SetCompatibility",
    "SetProtocolError",
    "SetUsageError",
    "SetVersion",
    "UnsupportedSetMediaTypeError",
    "capability_report",
    "compatibility",
    "compose_set_claim_set",
    "migrate_claims",
    "select_carrier",
    "select_version",
    "supports",
]
