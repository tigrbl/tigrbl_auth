"""Deprecated bridge for release signing helpers."""

from __future__ import annotations

import warnings

from tigrbl_identity_author.release_signing import *  # noqa: F403
from tigrbl_identity_author.release_signing import __all__, _canonical_json


warnings.warn(
    "tigrbl_identity_jose.release_signing is deprecated; use "
    "tigrbl_identity_author.release_signing.",
    DeprecationWarning,
    stacklevel=2,
)
