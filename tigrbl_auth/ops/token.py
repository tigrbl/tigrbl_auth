"""Compatibility facade for `tigrbl_identity_oauth.ops.token`.

This path is also loaded directly by a few legacy tests with
``importlib.util.spec_from_file_location``. Execute the canonical module into
this module namespace so monkeypatching legacy globals still affects functions
defined here.
"""

from importlib.util import find_spec as _find_spec
from pathlib import Path as _Path

from tigrbl_auth._split_imports import ensure_split_package_importable as _ensure_split

_ensure_split("tigrbl_identity_oauth", "tigrbl-identity-oauth")
_spec = _find_spec("tigrbl_identity_oauth.ops.token")
if _spec is None or _spec.origin is None:
    raise ModuleNotFoundError("tigrbl_identity_oauth.ops.token")
__file__ = _spec.origin
__package__ = "tigrbl_identity_oauth.ops"
__spec__ = _spec
exec(compile(_Path(_spec.origin).read_text(encoding="utf-8"), _spec.origin, "exec"), globals())
