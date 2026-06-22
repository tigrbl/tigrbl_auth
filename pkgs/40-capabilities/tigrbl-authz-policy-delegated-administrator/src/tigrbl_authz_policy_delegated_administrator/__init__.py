"""Storage-backed delegated administrator for the Tigrbl auth package suite."""

from .administrator import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    DelegatedAdministrator,
    DelegatedAdminScope,
)

__all__ = [
    "ADMIN_CLIENT_FIELDS",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "DelegatedAdministrator",
]
