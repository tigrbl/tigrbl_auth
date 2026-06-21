"""Compatibility module for RFC 8785 JSON canonicalization helpers.

Canonical module: tigrbl_identity_core.json_canonicalization.
"""

from __future__ import annotations

import warnings

from .json_canonicalization import (
    JCSCanonicalizationError,
    MAX_SAFE_INTEGER,
    RFC8785_SPEC_URL,
    canonicalize,
    canonicalize_json,
)

warnings.warn(
    "tigrbl_identity_core.rfc8785 is deprecated; use "
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
