"""Legacy import facade for Consent."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm.consent import Consent

__all__ = ["Consent"]
