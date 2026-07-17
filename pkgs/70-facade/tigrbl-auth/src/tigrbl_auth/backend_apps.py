"""Deprecated marker for backend-app composition moved to layer 90."""

from __future__ import annotations


class BackendAppCompositionMovedError(ImportError):
    """Raised when the retired layer-70 backend-app factory is called."""


def build_product_app(*args: object, **kwargs: object) -> object:
    raise BackendAppCompositionMovedError(
        "backend-app composition moved to tigrbl-auth-backend-app-core; "
        "backend applications must depend on that layer-90 package directly"
    )


__all__ = ["BackendAppCompositionMovedError", "build_product_app"]
