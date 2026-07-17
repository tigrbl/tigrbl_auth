"""JOSE wire operations mapped to protocol-neutral capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "jose",
        CURRENT_VERSION.identifier,
        "jose-jws-sign",
        "JWS protected header and payload",
        "artifact.protection",
        "sign",
        "jws",
    ),
    ProtocolCapabilityRequirement(
        "jose",
        CURRENT_VERSION.identifier,
        "jose-jws-verify",
        "JWS signature",
        "artifact.protection",
        "verify",
        "verified-jws",
    ),
    ProtocolCapabilityRequirement(
        "jose",
        CURRENT_VERSION.identifier,
        "jose-jwe-encrypt",
        "JWE protected header and plaintext",
        "artifact.protection",
        "encrypt",
        "jwe",
    ),
    ProtocolCapabilityRequirement(
        "jose",
        CURRENT_VERSION.identifier,
        "jose-jwe-decrypt",
        "JWE serialization",
        "artifact.protection",
        "decrypt",
        "decrypted-jwe",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
