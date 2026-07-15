"""OID4VCI wire operations mapped to issuance capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "oid4vci",
        CURRENT_VERSION.identifier,
        "oid4vci-configuration-registration",
        "credential_configuration_id",
        "digital-credential.issuance",
        "register_configuration",
        "credential-configuration",
    ),
    ProtocolCapabilityRequirement(
        "oid4vci",
        CURRENT_VERSION.identifier,
        "oid4vci-credential-offer",
        "credential_offer",
        "digital-credential.issuance",
        "create_offer",
        "credential-offer",
    ),
    ProtocolCapabilityRequirement(
        "oid4vci",
        CURRENT_VERSION.identifier,
        "oid4vci-wallet-attestation",
        "wallet attestation",
        "digital-credential.issuance",
        "verify_wallet_attestation",
        "verified-wallet-attestation",
        required=False,
    ),
    ProtocolCapabilityRequirement(
        "oid4vci",
        CURRENT_VERSION.identifier,
        "oid4vci-proof-decode",
        "proofs",
        "artifact.processing",
        "decode",
        "oid4vci-proof",
    ),
    ProtocolCapabilityRequirement(
        "oid4vci",
        CURRENT_VERSION.identifier,
        "oid4vci-proof-validation",
        "proofs",
        "artifact.processing",
        "validate",
        "verified-oid4vci-proof",
    ),
    ProtocolCapabilityRequirement(
        "oid4vci",
        CURRENT_VERSION.identifier,
        "oid4vci-credential-issuance",
        "credential request",
        "digital-credential.issuance",
        "issue",
        "credential-issuance-result",
    ),
    ProtocolCapabilityRequirement(
        "oid4vci",
        CURRENT_VERSION.identifier,
        "oid4vci-issuance-recording",
        "credential response",
        "digital-credential.issuance",
        "record_issuance",
        "credential-issuance-transaction",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
