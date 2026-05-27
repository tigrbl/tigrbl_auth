"""Legacy import facade for TokenRecord."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm.token_record import TokenRecord

__all__ = ["TokenRecord"]
