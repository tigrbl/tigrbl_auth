"""SD-JWT VC wire operations mapped to reportable capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "sd-jwt-vc",
        CURRENT_VERSION.identifier,
        "sd-jwt-vc-decode",
        "application/dc+sd-jwt",
        "artifact.processing",
        "decode",
        "sd-jwt-vc-disclosures",
    ),
    ProtocolCapabilityRequirement(
        "sd-jwt-vc",
        CURRENT_VERSION.identifier,
        "sd-jwt-vc-validation",
        "issuer-signed JWT and disclosures",
        "artifact.processing",
        "validate",
        "verified-sd-jwt-vc",
    ),
    ProtocolCapabilityRequirement(
        "sd-jwt-vc",
        CURRENT_VERSION.identifier,
        "sd-jwt-vc-encode",
        "application/dc+sd-jwt",
        "artifact.processing",
        "encode",
        "sd-jwt-vc",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
