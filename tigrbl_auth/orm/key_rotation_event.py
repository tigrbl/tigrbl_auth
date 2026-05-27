"""Legacy import facade for KeyRotationEvent."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm.key_rotation_event import KeyRotationEvent

__all__ = ["KeyRotationEvent"]
