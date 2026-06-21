"""Entity key helpers shared by identity packages."""

from __future__ import annotations


def tenant_key(tenant_id: str, entity_id: str) -> str:
    """Return the stable in-memory key for a tenant-scoped entity."""

    return f"{tenant_id}:{entity_id}"


def normalize_entity(entity_type: str, entity_id: str) -> str:
    """Return the normalized entity reference used by relationship graphs."""

    return f"{entity_type}:{entity_id}"


__all__ = ["normalize_entity", "tenant_key"]
