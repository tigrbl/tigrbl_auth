from __future__ import annotations

import warnings

warnings.warn(
    "tigrbl_security_trust_contracts is deprecated; use tigrbl_user_plane_contracts.security",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_user_plane_contracts.security import *
