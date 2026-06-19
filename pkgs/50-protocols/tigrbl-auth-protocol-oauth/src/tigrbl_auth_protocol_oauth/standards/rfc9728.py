"""RFC 9728 compatibility exports.

The protected-resource metadata route is owned by
``tigrbl_identity_storage.tables.token_record._protected_resource_metadata``.
"""

from __future__ import annotations

from tigrbl_identity_storage.tables.token_record._protected_resource_metadata import (
    include_rfc9728,
)
from tigrbl_identity_runtime.http_standards.well_known import WELL_KNOWN_ENDPOINTS

RFC9728_SPEC_URL = "https://www.rfc-editor.org/rfc/rfc9728"

__all__ = ["RFC9728_SPEC_URL", "WELL_KNOWN_ENDPOINTS", "include_rfc9728"]
