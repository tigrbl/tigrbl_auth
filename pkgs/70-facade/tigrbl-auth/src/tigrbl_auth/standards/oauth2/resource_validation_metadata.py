"""Compatibility exports for storage-runtime resource validation metadata routes."""

from __future__ import annotations

from tigrbl_identity_storage_runtime.metadata.resource_validation_metadata import (
    CAPABILITIES_METADATA_PATH,
    VERIFIER_CONTRACT_METADATA_PATH,
    include_resource_validation_metadata,
)

__all__ = [
    "CAPABILITIES_METADATA_PATH",
    "VERIFIER_CONTRACT_METADATA_PATH",
    "include_resource_validation_metadata",
]
