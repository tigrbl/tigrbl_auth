"""Compatibility facade for `tigrbl_identity_storage.db`."""

import sys
from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

import tigrbl_identity_storage.db as _module

sys.modules[__name__] = _module
globals().update(_module.__dict__)
