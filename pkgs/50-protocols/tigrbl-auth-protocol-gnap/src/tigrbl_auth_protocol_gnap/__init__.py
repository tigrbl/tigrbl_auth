"""Versioned RFC 9635 GNAP protocol ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import GNAP_SUBJECT_CLAIM_CLASSES, compose_gnap_subject_claim_set
from .compatibility import COMPATIBILITY_PATHS, GnapCompatibility, compatibility
from .errors import (
    GnapOperationUnavailableError,
    GnapProtocolError,
    GnapSchemaError,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_request
from .protocol import GnapProtocol
from .schemas import GnapRequest, parse_gnap_request, serialize_gnap_result
from .versions import CURRENT_VERSION, VERSION_HISTORY, GnapVersion, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="gnap",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_gnap_protocol.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "GNAP_SUBJECT_CLAIM_CLASSES",
    "VERSION_HISTORY",
    "GnapCompatibility",
    "GnapOperationUnavailableError",
    "GnapProtocol",
    "GnapProtocolError",
    "GnapRequest",
    "GnapSchemaError",
    "GnapVersion",
    "capability_report",
    "compatibility",
    "compose_gnap_subject_claim_set",
    "migrate_request",
    "parse_gnap_request",
    "select_version",
    "serialize_gnap_result",
    "supports",
]
