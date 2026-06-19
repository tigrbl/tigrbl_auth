from __future__ import annotations

import warnings

warnings.warn(
    "tigrbl_control_plane_contracts.admin_resources is deprecated; "
    "use tigrbl_management_plane_contracts.admin_resources",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_management_plane_contracts.admin_resources import *  # noqa: F401,F403
from tigrbl_management_plane_contracts.admin_resources import __all__ as __all__
