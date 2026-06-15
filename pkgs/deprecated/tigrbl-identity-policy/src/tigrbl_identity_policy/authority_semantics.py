"""Deprecated compatibility module for `tigrbl_authz_policy.authority_semantics`."""

from __future__ import annotations

from importlib import import_module as _import_module
import warnings as _warnings

_DEPRECATED_MODULE = "tigrbl_identity_policy.authority_semantics"
_CANONICAL_MODULE = "tigrbl_authz_policy.authority_semantics"

_warnings.warn(
    f"{_DEPRECATED_MODULE} is deprecated; import {_CANONICAL_MODULE} instead.",
    DeprecationWarning,
    stacklevel=2,
)

_target = _import_module(_CANONICAL_MODULE)
_EXCLUDED = {
    "__builtins__",
    "__cached__",
    "__file__",
    "__loader__",
    "__name__",
    "__package__",
    "__path__",
    "__spec__",
}
for _name, _value in vars(_target).items():
    if _name not in _EXCLUDED:
        globals()[_name] = _value

__all__ = list(getattr(_target, "__all__", [name for name in globals() if not name.startswith("_")]))