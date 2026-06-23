"""Contract-facing OpenAPI schema exports backed by identity storage tables."""

from __future__ import annotations

from tigrbl_identity_storage.schemas import *  # noqa: F403
from tigrbl_identity_storage.schemas import __all__ as _storage_schema_exports

__all__ = list(_storage_schema_exports)
