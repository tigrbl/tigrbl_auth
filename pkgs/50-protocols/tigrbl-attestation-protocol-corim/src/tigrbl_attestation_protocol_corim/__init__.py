from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement
from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report

from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_document
from .versions import CURRENT_VERSION, VERSION_HISTORY, CorimVersion, select_version


CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        protocol="corim",
        revision=CURRENT_VERSION.identifier,
        requirement_id="corim-reference-publication",
        wire_element="tag-identity",
        capability_id="attestation.reference-material",
        operation="publish",
        normalized_namespace="attestation-reference-manifest",
    ),
    ProtocolCapabilityRequirement(
        protocol="corim",
        revision=CURRENT_VERSION.identifier,
        requirement_id="corim-appraisal-consumption",
        wire_element="tags",
        capability_id="attestation.appraisal",
        operation="appraise",
        normalized_namespace="attestation-evidence",
    ),
)


def capability_report() -> dict[str, object]:
    report = build_protocol_capability_report(
        protocol="corim",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_corim_protocol_versioning.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
    )
    report["status"] = CURRENT_VERSION.status
    report["unsupported"] = (
        "trust-anchor-selection", "key-loading", "appraisal-policy-selection"
    )
    return report


__all__ = [
    "CAPABILITY_REQUIREMENTS", "CURRENT_VERSION", "FEATURES_BY_VERSION",
    "VERSION_HISTORY", "CorimVersion", "capability_report", "migrate_document",
    "select_version", "supports",
]
