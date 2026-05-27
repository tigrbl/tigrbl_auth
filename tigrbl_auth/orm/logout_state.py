"""Legacy import facade for LogoutState."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm.logout_state import LogoutState

__all__ = ["LogoutState"]
