"""CoRIM artifact operations mapped to semantic capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "corim",
        CURRENT_VERSION.identifier,
        "corim-cbor-decode",
        "signed or unsigned CoRIM CBOR",
        "artifact.processing",
        "decode",
        "corim-reference-manifest",
    ),
    ProtocolCapabilityRequirement(
        "corim",
        CURRENT_VERSION.identifier,
        "corim-validation",
        "CoRIM/CoMID/CoSWID/CoTL/CoTS",
        "artifact.processing",
        "validate",
        "validated-reference-manifest",
    ),
    ProtocolCapabilityRequirement(
        "corim",
        CURRENT_VERSION.identifier,
        "corim-cbor-encode",
        "signed or unsigned CoRIM CBOR",
        "artifact.processing",
        "encode",
        "corim",
    ),
    ProtocolCapabilityRequirement(
        "corim",
        CURRENT_VERSION.identifier,
        "corim-reference-resolution",
        "tag-identity",
        "attestation.appraisal",
        "resolve_reference_material",
        "attestation-reference-manifest",
    ),
    ProtocolCapabilityRequirement(
        "corim",
        CURRENT_VERSION.identifier,
        "corim-appraisal-consumption",
        "reference values and endorsements",
        "attestation.appraisal",
        "appraise",
        "attestation-appraisal-result",
        required=False,
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
