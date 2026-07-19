from .protocol import JwtProtocol
"""Versioned RFC 7519 JSON Web Token ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import JWT_CLAIM_CLASSES, JWT_VERSION, compose_jwt_claim_set
from .compatibility import COMPATIBILITY_PATHS, JwtCompatibility, compatibility
from .errors import JwtProfileRequiredError, JwtProtocolError, UnsupportedJwtMediaTypeError
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .profile import JwtProfile
from .schemas import JWT_CARRIER, JwtCarrier, select_carrier
from .versions import CURRENT_VERSION, VERSION_HISTORY, JwtVersion, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="jwt",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_jwt_protocol.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "JwtProtocol",
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "JWT_CARRIER",
    "JWT_CLAIM_CLASSES",
    "JWT_VERSION",
    "VERSION_HISTORY",
    "JwtCarrier",
    "JwtCompatibility",
    "JwtProfile",
    "JwtProfileRequiredError",
    "JwtProtocolError",
    "JwtVersion",
    "UnsupportedJwtMediaTypeError",
    "capability_report",
    "compatibility",
    "compose_jwt_claim_set",
    "migrate_claims",
    "select_carrier",
    "select_version",
    "supports",
]
