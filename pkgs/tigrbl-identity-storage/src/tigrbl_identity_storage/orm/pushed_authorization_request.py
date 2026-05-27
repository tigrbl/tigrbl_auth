"""ORM import facade for canonical table module."""

from tigrbl_identity_storage.tables.pushed_authorization_request import (
    DEFAULT_PAR_EXPIRY,
    PushedAuthorizationRequest,
)

__all__ = ["PushedAuthorizationRequest", "DEFAULT_PAR_EXPIRY"]
