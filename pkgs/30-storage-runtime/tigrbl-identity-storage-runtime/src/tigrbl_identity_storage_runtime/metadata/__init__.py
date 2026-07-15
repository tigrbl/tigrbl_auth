"""Runtime metadata route publishers for identity storage-backed surfaces."""

from .protected_resource_metadata import (
    RFC9728_SPEC_URL,
    build_protected_resource_metadata,
    include_rfc9728,
)
from .resource_validation_metadata import (
    CAPABILITIES_METADATA_PATH,
    VERIFIER_CONTRACT_METADATA_PATH,
    include_resource_validation_metadata,
)

__all__ = [
    "CAPABILITIES_METADATA_PATH",
    "RFC9728_SPEC_URL",
    "VERIFIER_CONTRACT_METADATA_PATH",
    "build_protected_resource_metadata",
    "include_resource_validation_metadata",
    "include_rfc9728",
]
