"""Release-path OAuth token endpoint surface."""

from tigrbl_identity_storage.tables.token_record import api, router, token

__all__ = ["api", "router", "token"]
