"""Versioned OpenID for Verifiable Presentations ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import OID4VP_BINDING_CLAIM_CLASSES, compose_oid4vp_binding_claim_set
from .compatibility import (
    COMPATIBILITY_PATHS,
    Oid4vpCompatibility,
    compatibility,
)
from .errors import (
    Oid4vpProtocolError,
    Oid4vpRequestBindingError,
    UnsupportedPresentationFormatError,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_request
from .protocol import Oid4vpProtocol
from .schemas import Oid4vpAuthorizationRequest, Oid4vpDirectPostResponse
from .versions import CURRENT_VERSION, VERSION_HISTORY, Oid4vpVersion, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="oid4vp",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_oid4vc_authzen_protocols.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "OID4VP_BINDING_CLAIM_CLASSES",
    "VERSION_HISTORY",
    "Oid4vpAuthorizationRequest",
    "Oid4vpCompatibility",
    "Oid4vpDirectPostResponse",
    "Oid4vpProtocol",
    "Oid4vpProtocolError",
    "Oid4vpRequestBindingError",
    "Oid4vpVersion",
    "UnsupportedPresentationFormatError",
    "capability_report",
    "compatibility",
    "compose_oid4vp_binding_claim_set",
    "migrate_request",
    "select_version",
    "supports",
]
