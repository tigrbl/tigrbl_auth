"""Legacy import facade for AuditEvent."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm.audit_event import AuditEvent

__all__ = ["AuditEvent"]
