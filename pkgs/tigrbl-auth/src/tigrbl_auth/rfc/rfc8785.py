"""Deprecated RFC 8785 compatibility import path."""

from __future__ import annotations

import warnings

from tigrbl_identity_core.json_canonicalization import (
    JCSCanonicalizationError,
    MAX_SAFE_INTEGER,
    RFC8785_SPEC_URL,
    canonicalize,
    canonicalize_json,
)

warnings.warn(
    "tigrbl_auth.rfc.rfc8785 is deprecated; use "
    "tigrbl_identity_core.json_canonicalization instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "JCSCanonicalizationError",
    "MAX_SAFE_INTEGER",
    "RFC8785_SPEC_URL",
    "canonicalize",
    "canonicalize_json",
]
