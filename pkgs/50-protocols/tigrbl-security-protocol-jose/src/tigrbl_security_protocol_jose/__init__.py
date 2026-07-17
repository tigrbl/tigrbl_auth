"""Versioned JOSE protocol-family ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import CLAIMS_ARE_PROFILE_OWNED, JOSE_CLAIM_CLASSES
from .compatibility import COMPATIBILITY_PATHS, JoseCompatibility, compatibility
from .errors import (
    JoseProtocolError,
    UnsupportedJoseMediaTypeError,
    UnsupportedJoseMigrationError,
)
from .features import FEATURES_BY_VERSION, JoseFeatures, supports
from .migrations import migrate_configuration
from .schemas import (
    JOSE_CARRIERS,
    JoseArtifactKind,
    JoseCarrier,
    JoseSerialization,
    select_carrier,
)
from .versions import (
    CURRENT_VERSION,
    JOSE_SPECIFICATIONS,
    VERSION_HISTORY,
    JoseSpecification,
    JoseVersion,
    select_version,
)


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="jose",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_jose_protocol.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "CLAIMS_ARE_PROFILE_OWNED",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "JOSE_CARRIERS",
    "JOSE_CLAIM_CLASSES",
    "JOSE_SPECIFICATIONS",
    "VERSION_HISTORY",
    "JoseArtifactKind",
    "JoseCarrier",
    "JoseCompatibility",
    "JoseFeatures",
    "JoseProtocolError",
    "JoseSerialization",
    "JoseSpecification",
    "JoseVersion",
    "UnsupportedJoseMediaTypeError",
    "UnsupportedJoseMigrationError",
    "capability_report",
    "compatibility",
    "migrate_configuration",
    "select_carrier",
    "select_version",
    "supports",
]
