"""Compatibility facade for canonical identity storage ORM imports."""

from __future__ import annotations

import sys

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm import auth_code as _canonical_module
from tigrbl_identity_storage.orm.auth_code import AuthCode, _jwt, mint_id_token

sys.modules[__name__] = _canonical_module

__all__ = ["AuthCode", "_jwt", "mint_id_token"]
