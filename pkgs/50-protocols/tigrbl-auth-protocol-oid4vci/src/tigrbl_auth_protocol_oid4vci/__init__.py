"""Versioned OpenID for Verifiable Credential Issuance ownership."""

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import OID4VCI_PROOF_CLAIM_CLASSES, compose_oid4vci_proof_claim_set
from .compatibility import (
    COMPATIBILITY_PATHS,
    Oid4vciCompatibility,
    compatibility,
)
from .errors import (
    Oid4vciProofError,
    Oid4vciProtocolError,
    UnsupportedCredentialConfigurationError,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_request
from .protocol import Oid4vciProtocol
from .schemas import Oid4vciCredentialRequest, Oid4vciCredentialResponse
from .versions import CURRENT_VERSION, VERSION_HISTORY, Oid4vciVersion, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="oid4vci",
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
    "OID4VCI_PROOF_CLAIM_CLASSES",
    "VERSION_HISTORY",
    "Oid4vciCompatibility",
    "Oid4vciCredentialRequest",
    "Oid4vciCredentialResponse",
    "Oid4vciProofError",
    "Oid4vciProtocol",
    "Oid4vciProtocolError",
    "Oid4vciVersion",
    "UnsupportedCredentialConfigurationError",
    "capability_report",
    "compatibility",
    "compose_oid4vci_proof_claim_set",
    "migrate_request",
    "select_version",
    "supports",
]
