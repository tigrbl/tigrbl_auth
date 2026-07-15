"""HAIP profile requirements mapped to composed capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "haip",
        CURRENT_VERSION.identifier,
        "haip-credential-issuance",
        "OID4VCI credential response",
        "digital-credential.issuance",
        "issue",
        "haip-credential",
    ),
    ProtocolCapabilityRequirement(
        "haip",
        CURRENT_VERSION.identifier,
        "haip-wallet-attestation",
        "wallet attestation",
        "digital-credential.issuance",
        "verify_wallet_attestation",
        "verified-wallet-attestation",
    ),
    ProtocolCapabilityRequirement(
        "haip",
        CURRENT_VERSION.identifier,
        "haip-presentation",
        "OID4VP authorization response",
        "digital-credential.presentation",
        "present",
        "haip-presentation-result",
    ),
    ProtocolCapabilityRequirement(
        "haip",
        CURRENT_VERSION.identifier,
        "haip-presentation-verification",
        "SD-JWT VC or mdoc presentation",
        "digital-credential.presentation",
        "verify_presentation",
        "verified-haip-presentation",
    ),
    ProtocolCapabilityRequirement(
        "haip",
        CURRENT_VERSION.identifier,
        "haip-artifact-validation",
        "SD-JWT VC, KB-JWT, mdoc, or attestation artifact",
        "artifact.processing",
        "validate",
        "verified-haip-artifact",
    ),
    ProtocolCapabilityRequirement(
        "haip",
        CURRENT_VERSION.identifier,
        "haip-key-verifier-attestation",
        "key or verifier attestation",
        "attestation.appraisal",
        "verify_evidence",
        "verified-attestation-evidence",
    ),
    ProtocolCapabilityRequirement(
        "haip",
        CURRENT_VERSION.identifier,
        "haip-replay-protection",
        "nonce and transaction binding",
        "security.replay-protection",
        "check_and_reserve",
        "haip:presentation-binding",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
