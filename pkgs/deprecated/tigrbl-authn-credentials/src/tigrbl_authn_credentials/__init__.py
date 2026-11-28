"""Deprecated compatibility facade for :mod:`tigrbl_credentials`."""

from __future__ import annotations

from importlib import import_module as _import_module
import warnings as _warnings

_warnings.warn(
    "tigrbl_authn_credentials is deprecated; import tigrbl_credentials instead.",
    DeprecationWarning,
    stacklevel=2,
)

_target = _import_module("tigrbl_credentials")
_EXCLUDED = {
    "__builtins__", "__cached__", "__file__", "__loader__", "__name__",
    "__package__", "__path__", "__spec__",
}
for _name, _value in vars(_target).items():
    if _name not in _EXCLUDED:
        globals()[_name] = _value

__all__ = list(getattr(_target, "__all__", ()))
