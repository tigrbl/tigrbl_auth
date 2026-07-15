"""RFC 8392 wire operations mapped to reportable capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "cwt",
        CURRENT_VERSION.value,
        "cwt-cbor-decode",
        "CBOR map",
        "artifact.processing",
        "decode",
        "cwt-claims",
    ),
    ProtocolCapabilityRequirement(
        "cwt",
        CURRENT_VERSION.value,
        "cwt-cose-validation",
        "COSE protected CWT",
        "artifact.processing",
        "validate",
        "protected-token-envelope",
    ),
    ProtocolCapabilityRequirement(
        "cwt",
        CURRENT_VERSION.value,
        "cwt-cbor-encode",
        "application/cwt",
        "artifact.processing",
        "encode",
        "cwt",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
