"""Compatibility exports for resource-validation metadata publication."""

from __future__ import annotations

from tigrbl_identity_contracts.resource_validation_metadata import (
    CAPABILITIES_METADATA_PATH,
    VERIFIER_CONTRACT_METADATA_PATH,
)
from tigrbl_identity_server.resource_validation_metadata_surface import (
    include_resource_validation_metadata,
)

__all__ = [
    "CAPABILITIES_METADATA_PATH",
    "VERIFIER_CONTRACT_METADATA_PATH",
    "include_resource_validation_metadata",
]
