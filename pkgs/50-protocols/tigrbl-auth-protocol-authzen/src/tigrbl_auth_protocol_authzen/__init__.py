"""Versioned OpenID AuthZEN Authorization API ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import AUTHZEN_CLAIM_CLASSES
from .compatibility import (
    COMPATIBILITY_PATHS,
    AuthzenCompatibility,
    compatibility,
)
from .errors import (
    AuthzenOperationUnavailableError,
    AuthzenProtocolError,
    AuthzenSchemaError,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_evaluation
from .protocol import AuthzenProtocol
from .schemas import (
    AuthzenPdpMetadata,
    parse_evaluation_request,
    parse_search_request,
    serialize_evaluation_result,
    serialize_search_result,
)
from .versions import AuthzenVersion, CURRENT_VERSION, VERSION_HISTORY, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="authzen",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_oid4vc_authzen_protocols.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "AUTHZEN_CLAIM_CLASSES",
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "VERSION_HISTORY",
    "AuthzenCompatibility",
    "AuthzenOperationUnavailableError",
    "AuthzenPdpMetadata",
    "AuthzenProtocol",
    "AuthzenProtocolError",
    "AuthzenSchemaError",
    "AuthzenVersion",
    "capability_report",
    "compatibility",
    "migrate_evaluation",
    "parse_evaluation_request",
    "parse_search_request",
    "select_version",
    "serialize_evaluation_result",
    "serialize_search_result",
    "supports",
]
