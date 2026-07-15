"""Runtime metadata route publishers for identity storage-backed surfaces."""

from .resource_validation_metadata import (
    CAPABILITIES_METADATA_PATH,
    VERIFIER_CONTRACT_METADATA_PATH,
    include_resource_validation_metadata,
)

__all__ = [
    "CAPABILITIES_METADATA_PATH",
    "VERIFIER_CONTRACT_METADATA_PATH",
    "include_resource_validation_metadata",
]
