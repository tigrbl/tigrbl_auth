from __future__ import annotations

from .operator_service import (
    create_resource,
    delete_resource,
    get_resource,
    list_resource_result,
    lock_identity,
    set_identity_password,
    update_resource,
)

__all__ = [
    "create_resource",
    "delete_resource",
    "get_resource",
    "list_resource_result",
    "lock_identity",
    "set_identity_password",
    "update_resource",
]
