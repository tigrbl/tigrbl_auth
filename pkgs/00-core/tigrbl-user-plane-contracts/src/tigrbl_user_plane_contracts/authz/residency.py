from __future__ import annotations

import warnings

warnings.warn(
    "tigrbl_user_plane_contracts.authz.residency is deprecated; "
    "use tigrbl_management_plane_contracts.residency",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_management_plane_contracts.residency import *  # noqa: F401,F403
from tigrbl_management_plane_contracts.residency import __all__ as __all__
