"""RFC 9711 wire elements mapped to reportable capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "eat",
        CURRENT_VERSION.identifier,
        "eat-protected-token-verification",
        "application/eat+jwt application/eat+cwt",
        "attestation.appraisal",
        "verify_evidence",
        "attestation-evidence",
    ),
    ProtocolCapabilityRequirement(
        "eat",
        CURRENT_VERSION.identifier,
        "eat-reference-backed-appraisal",
        "eat_profile",
        "attestation.appraisal",
        "appraise",
        "verified-attestation-evidence",
    ),
    ProtocolCapabilityRequirement(
        "eat",
        CURRENT_VERSION.identifier,
        "eat-reference-resolution",
        "eat_profile",
        "attestation.appraisal",
        "resolve_reference_material",
        "attestation-reference-manifest",
        required=False,
    ),
    ProtocolCapabilityRequirement(
        "eat",
        CURRENT_VERSION.identifier,
        "eat-appraisal-recording",
        "appraisal-result",
        "attestation.appraisal",
        "record_result",
        "attestation-result",
        required=False,
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
