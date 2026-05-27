"""Compatibility facade for ``tigrbl_identity_storage.tables.audit_event``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.audit_event import AuditEvent

__all__ = ["AuditEvent"]
