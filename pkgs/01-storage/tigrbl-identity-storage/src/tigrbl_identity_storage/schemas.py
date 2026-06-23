"""OpenAPI-named schemas derived from storage table bindings."""

from __future__ import annotations

from .schema_registry import OPENAPI_SCHEMA_REGISTRY

globals().update(OPENAPI_SCHEMA_REGISTRY)

__all__ = sorted(OPENAPI_SCHEMA_REGISTRY)
