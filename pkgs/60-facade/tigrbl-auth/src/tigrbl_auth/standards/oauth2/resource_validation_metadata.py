"""Compatibility exports for storage-owned resource validation metadata routes."""

from __future__ import annotations

from tigrbl_identity_storage.tables._resource_validation_metadata import (
    CAPABILITIES_METADATA_PATH,
    VERIFIER_CONTRACT_METADATA_PATH,
    include_resource_validation_metadata,
)

__all__ = [
    "CAPABILITIES_METADATA_PATH",
    "VERIFIER_CONTRACT_METADATA_PATH",
    "include_resource_validation_metadata",
]
