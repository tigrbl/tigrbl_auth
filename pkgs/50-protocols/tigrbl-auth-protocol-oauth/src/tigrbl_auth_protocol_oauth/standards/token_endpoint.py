"""Release-path OAuth token endpoint surface."""

from tigrbl_identity_storage_runtime.token_endpoint import router, token

api = router

__all__ = ["api", "router", "token"]
