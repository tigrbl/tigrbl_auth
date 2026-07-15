"""Versioned High Assurance Interoperability Profile ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import HAIP_PROOF_CLAIM_CLASSES
from .compatibility import COMPATIBILITY_PATHS, HaipCompatibility, compatibility
from .errors import HaipComponentVersionError, HaipProfileError, HaipTrustBindingError
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_configuration
from .profile import HAIP_CREDENTIAL_FORMATS, HaipConfiguration, configure_haip
from .schemas import HaipComponentVersions, HaipCredentialFormats
from .versions import CURRENT_VERSION, VERSION_HISTORY, HaipVersion, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="haip",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_haip_profile.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "HAIP_CREDENTIAL_FORMATS",
    "HAIP_PROOF_CLAIM_CLASSES",
    "VERSION_HISTORY",
    "HaipCompatibility",
    "HaipComponentVersionError",
    "HaipComponentVersions",
    "HaipConfiguration",
    "HaipCredentialFormats",
    "HaipProfileError",
    "HaipTrustBindingError",
    "HaipVersion",
    "capability_report",
    "compatibility",
    "configure_haip",
    "migrate_configuration",
    "select_version",
    "supports",
]
