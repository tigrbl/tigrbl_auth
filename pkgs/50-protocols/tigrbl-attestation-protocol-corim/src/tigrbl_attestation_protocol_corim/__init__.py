"""Versioned CoRIM-family reference-material profile ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import CORIM_CLAIM_CLASSES, CORIM_MAP_FIELDS
from .compatibility import COMPATIBILITY_PATHS, CorimCompatibility, compatibility
from .errors import (
    CorimProtocolError,
    CorimReferenceIntegrityError,
    UnsupportedCorimMediaTypeError,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_document
from .schemas import (
    CORIM_CARRIERS,
    CORIM_SIGNED_CARRIER,
    CORIM_UNSIGNED_CARRIER,
    CorimCarrier,
    select_carrier,
)
from .versions import CURRENT_VERSION, VERSION_HISTORY, CorimVersion, select_version


def capability_report() -> dict[str, object]:
    report = build_protocol_capability_report(
        protocol="corim",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_corim_protocol_versioning.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )
    report["status"] = CURRENT_VERSION.status
    return report


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CORIM_CARRIERS",
    "CORIM_CLAIM_CLASSES",
    "CORIM_MAP_FIELDS",
    "CORIM_SIGNED_CARRIER",
    "CORIM_UNSIGNED_CARRIER",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "VERSION_HISTORY",
    "CorimCarrier",
    "CorimCompatibility",
    "CorimProtocolError",
    "CorimReferenceIntegrityError",
    "CorimVersion",
    "UnsupportedCorimMediaTypeError",
    "capability_report",
    "compatibility",
    "migrate_document",
    "select_carrier",
    "select_version",
    "supports",
]
