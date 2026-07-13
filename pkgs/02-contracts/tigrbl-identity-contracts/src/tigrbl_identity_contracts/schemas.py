"""Deprecated lazy compatibility access to storage-owned API schemas."""

from __future__ import annotations

from importlib import import_module
import warnings


def _owner():
    return import_module("tigrbl_identity_storage.schemas")


def __getattr__(name: str):
    warnings.warn(
        "tigrbl_identity_contracts.schemas is deprecated; import storage-owned "
        "operation schemas from tigrbl_identity_storage.schemas",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_owner(), name)


__all__ = list(getattr(_owner(), "__all__", ()))
