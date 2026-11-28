"""TBA plugin adoption adapter."""

from typing import TYPE_CHECKING

from .operation_adapter import (
    OperationAuthorizationAdapter,
    OperationPolicy,
    OperationPrincipal,
    operation_catalog_digest,
)

if TYPE_CHECKING:
    from .plugin import TbaPlugin, install


def __getattr__(name: str):
    if name in {"TbaPlugin", "install"}:
        from . import plugin

        return getattr(plugin, name)
    raise AttributeError(name)

__all__ = [
    "OperationAuthorizationAdapter",
    "OperationPolicy",
    "OperationPrincipal",
    "TbaPlugin",
    "install",
    "operation_catalog_digest",
]
