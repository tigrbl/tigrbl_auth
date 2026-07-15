"""Authorization API 1.0 operations mapped to reportable capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "authzen",
        CURRENT_VERSION.identifier,
        "access-evaluation",
        "/access/v1/evaluation",
        "policy.evaluation",
        "evaluate",
        "policy-evaluation",
    ),
    ProtocolCapabilityRequirement(
        "authzen",
        CURRENT_VERSION.identifier,
        "access-evaluations",
        "/access/v1/evaluations",
        "policy.evaluation",
        "evaluate_many",
        "policy-evaluations",
        False,
    ),
    ProtocolCapabilityRequirement(
        "authzen",
        CURRENT_VERSION.identifier,
        "search-subject",
        "/access/v1/search/subject",
        "policy.evaluation",
        "search_entities",
        "policy-subjects",
        False,
    ),
    ProtocolCapabilityRequirement(
        "authzen",
        CURRENT_VERSION.identifier,
        "search-resource",
        "/access/v1/search/resource",
        "policy.evaluation",
        "search_entities",
        "policy-resources",
        False,
    ),
    ProtocolCapabilityRequirement(
        "authzen",
        CURRENT_VERSION.identifier,
        "search-action",
        "/access/v1/search/action",
        "policy.evaluation",
        "search_entities",
        "policy-actions",
        False,
    ),
    ProtocolCapabilityRequirement(
        "authzen",
        CURRENT_VERSION.identifier,
        "pdp-configuration",
        "/.well-known/authzen-configuration",
        "policy.evaluation",
        "describe",
        "policy-service-description",
        False,
    ),
    ProtocolCapabilityRequirement(
        "authzen",
        CURRENT_VERSION.identifier,
        "signed-metadata",
        "signed_metadata",
        "artifact.processing",
        "validate",
        "verified-authzen-metadata",
        False,
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
